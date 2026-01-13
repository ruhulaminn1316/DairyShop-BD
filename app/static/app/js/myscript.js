// myscript.js – Modern, Clean & Professional (2025 Standard)
// Compatible with your Django e-commerce project

document.addEventListener('DOMContentLoaded', function () {

    // =============================================
    // 1. OWL CAROUSEL – Multiple Sliders (Responsive + Autoplay)
    // =============================================
    const sliders = document.querySelectorAll('#slider1, #slider2, #slider3');
    sliders.forEach(slider => {
        if (slider) {
            $(slider).owlCarousel({
                loop: true,
                margin: 20,
                nav: true,
                autoplay: true,
                autoplayTimeout: 4000,
                autoplayHoverPause: true,
                responsiveClass: true,
                responsive: {
                    0: { items: 2, nav: false },
                    600: { items: 4, nav: true },
                    1000: { items: 6, nav: true }
                },
                navText: ['<i class="bi bi-chevron-left"></i>', '<i class="bi bi-chevron-right"></i>'],
                dots: false
            });
        }
    });

    // =============================================
    // 2. CART FUNCTIONS – Plus, Minus, Remove
    // =============================================
    function updateCart(action, button) {
        const prodId = button.getAttribute('pid');
        const quantityElement = button.parentNode.querySelector('.quantity') || button.parentNode.children[2];

        fetch(`/cart/${action}`, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Update quantity
                if (quantityElement) {
                    quantityElement.textContent = data.quantity;
                }

                // Update totals
                const amountEl = document.getElementById('amount');
                const totalEl = document.getElementById('totalamount');
                if (amountEl) amountEl.textContent = data.amount;
                if (totalEl) totalEl.textContent = data.totalamount;

                // Remove item if quantity is 0
                if (action === 'removecart' && data.quantity === 0) {
                    button.closest('.cart-item')?.remove() || 
                    button.parentNode.parentNode.parentNode.parentNode.remove();
                }
            } else {
                alert(data.message || 'Something went wrong!');
            }
        })
        .catch(err => {
            console.error('Error:', err);
            alert('Failed to update cart. Please try again.');
        });
    }

    // Plus Cart
    document.querySelectorAll('.plus-cart').forEach(btn => {
        btn.addEventListener('click', function () {
            updateCart('pluscart', this);
        });
    });

    // Minus Cart
    document.querySelectorAll('.minus-cart').forEach(btn => {
        btn.addEventListener('click', function () {
            updateCart('minuscart', this);
        });
    });

    // Remove from Cart
    document.querySelectorAll('.remove-cart').forEach(btn => {
        btn.addEventListener('click', function () {
            if (confirm('Are you sure you want to remove this item?')) {
                updateCart('removecart', this);
            }
        });
    });

    // =============================================
    // 3. WISHLIST FUNCTIONS – Add / Remove
    // =============================================
    function updateWishlist(action, button) {
        const prodId = button.getAttribute('pid');

        fetch(`/wishlist/${action}`, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Redirect to product detail after wishlist action
                window.location.href = `/product-detail/${prodId}`;
            } else {
                alert(data.message || 'Could not update wishlist.');
            }
        })
        .catch(err => {
            console.error('Wishlist Error:', err);
            alert('Failed to update wishlist.');
        });
    }

    document.querySelectorAll('.plus-wishlist').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            updateWishlist('pluswishlist', this);
        });
    });

    document.querySelectorAll('.minus-wishlist').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            updateWishlist('minuswishlist', this);
        });
    });

    // =============================================
    // 4. TOAST NOTIFICATION (Optional Enhancement)
    // =============================================
    function showToast(message, type = 'success') {
        const toast = document.getElementById('django-toast-body');
        if (toast) {
            toast.textContent = message;
            toast.parentElement.parentElement.classList.remove('bg-success', 'bg-danger', 'bg-info');
            toast.parentElement.parentElement.classList.add(type === 'success' ? 'bg-success' : 'bg-danger');
            new bootstrap.Toast(document.getElementById('django-toast')).show();
        }
    }

    // You can call showToast("Added to cart!") anywhere if needed
});