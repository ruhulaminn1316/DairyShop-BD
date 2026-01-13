from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decimal import Decimal
import json
import requests

from .models import Product, Cart, Wishlist, Order, Transaction


# ===============================
# 🏠 HOME
# ===============================
def home(request):
    products = Product.objects.all()
    return render(request, 'app/index.html', {'products': products})


# ===============================
# 🧀 CATEGORY
# ===============================
class CategoryView(View):
    def get(self, request, val):
        products = Product.objects.filter(category=val)
        return render(request, 'app/category.html', {'products': products, 'val': val})


# ===============================
# 📦 PRODUCT DETAILS
# ===============================
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app/productdetails.html', {'product': product})


# ===============================
# 📞 CONTACT
# ===============================
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        try:
            send_mail(
                f"New Contact Message: {subject}",
                f"From: {name} <{email}>\n\n{message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
            )
            messages.success(request, "Your message has been sent successfully!")
        except:
            messages.error(request, "Something went wrong.")
        return redirect('contact')

    return render(request, 'app/contact.html')


# ===============================
# ℹ️ ABOUT
# ===============================
def about(request):
    return render(request, 'app/about.html')


# ===============================
# 🛒 CART
# ===============================
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product added to cart")
    return redirect('cart')


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.discounted_price * item.quantity for item in cart_items)
    return render(request, 'app/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, cart_id):
    Cart.objects.filter(id=cart_id, user=request.user).delete()
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if request.method == "POST":
        cart_item.quantity = int(request.POST.get("quantity", 1))
        cart_item.save()
    return redirect('cart')


# ===============================
# 💖 WISHLIST
# ===============================
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': items})


@login_required
def remove_from_wishlist(request, item_id):
    Wishlist.objects.filter(id=item_id, user=request.user).delete()
    return redirect('wishlist')

# ===============================
# 🛍️ BUY NOW (FINAL & CLEAN)
# ===============================
@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        address = request.POST.get("address")

        if not address:
            messages.error(request, "Shipping address is required.")
            return redirect('buy_now', product_id=product.id)

        # ✅ Create Order
        order = Order.objects.create(
            user=request.user,
            product=product,
            total=product.discounted_price,
            shipping_address=address,
            status='pending'
        )

        # 📧 EMAIL TO ADMIN
        send_mail(
            subject=f"🛒 New Order Received | Order #{order.id}",
            message=f"""
New order placed!

Order ID: {order.id}
Customer: {request.user.username}
Email: {request.user.email}

Product: {product.title}
Price: ৳{product.discounted_price}

Shipping Address:
{address}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['sharatacharjee6@gmail.com'],
            fail_silently=False
        )

        messages.success(request, "Order placed successfully! Waiting for admin approval.")
        return redirect('my_orders')

    return render(request, 'app/buy_now.html', {"product": product})

# ===============================
# 📦 MY ORDERS (USER)
# ===============================
from django.db import models

from django.db import models

@login_required
def my_orders(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .exclude(status='cancelled')   # ❌ cancelled hide
        .order_by(
            models.Case(
                models.When(status='pending', then=0),
                models.When(status='accepted', then=1),
                models.When(status='paid', then=2),
                default=3,
                output_field=models.IntegerField()
            ),
            '-created_at'
        )
    )

    return render(request, 'app/my_orders.html', {'orders': orders})



# ===============================
# ❌ CANCEL ORDER (USER – Pending only)
# ===============================
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != 'pending':
        messages.error(request, "Only pending orders can be cancelled.")
        return redirect('my_orders')

    order.status = 'cancelled'
    order.save()

    messages.success(request, "Order cancelled successfully.")
    return redirect('my_orders')

# ===============================
# 🔍 SEARCH
# ===============================
def search(request):
    q = request.GET.get("query", "")
    products = Product.objects.filter(
        Q(title__icontains=q) | Q(description__icontains=q)
    )
    return render(request, 'app/search_results.html', {
        'products': products,
        'query': q
    })


# ===============================
# 👨‍💼 ADMIN: ACCEPT / REJECT ORDER + EMAIL
# ===============================
@login_required
@user_passes_test(lambda u: u.is_staff)
def update_order_status(request, order_id, status):
    if status not in ['accepted', 'rejected']:
        messages.error(request, "Invalid status")
        return redirect('admin_dashboard')

    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()

    # 📧 EMAIL USER
    send_mail(
        subject=f"Order #{order.id} {status.capitalize()}",
        message=f"""
Hello {order.user.username},

Your order has been {status}.

Product: {order.product.title}
Order ID: {order.id}
Total Amount: ৳{order.total}

Thank you for shopping with Daily Dairy Shop.
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.user.email],
        fail_silently=True,
    )

    messages.success(request, f"Order #{order.id} {status.upper()} successfully.")
    return redirect('admin_dashboard')


# ===============================
# 👨‍💼 ADMIN DASHBOARD (PROFESSIONAL)
# ===============================
from django.utils import timezone
from django.db.models import Sum
from .models import Order, Product

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    orders = Order.objects.select_related('user', 'product').order_by('-created_at')
    products = Product.objects.all()

    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today).count()

    total_revenue = Order.objects.filter(
        status__in=['accepted', 'paid']
    ).aggregate(total=Sum('total'))['total'] or 0

    context = {
        'orders': orders,
        'products': products,
        'today_orders': today_orders,
        'total_revenue': total_revenue,
        'today': today,
    }

    return render(request, 'app/admin_dashboard.html', context)



