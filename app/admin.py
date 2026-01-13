from django.contrib import admin
from .models import Product, Order

# ===============================
# 🛒 PRODUCT ADMIN
# ===============================
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'selling_price',
        'discounted_price',
        'category',
        'image'
    ]
    list_filter = ['category']
    search_fields = ['title', 'description']
    prepopulated_fields = {"slug": ("title",)}  # optional but useful


# ===============================
# 📦 ORDER ADMIN (IMPORTANT)
# ===============================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'product',
        'total',
        'status',
        'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = [
        'user__username',
        'product__title'
    ]
    ordering = ['-created_at']
