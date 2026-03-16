document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    console.log('ShopHub E-Commerce Platform loaded successfully');
});

function updateCartCount() {
    const cart = StorageManager.getCart();
    const cartCount = document.getElementById('cart-count');
    
    if (cartCount) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
    }
}

window.updateCartCount = updateCartCount;
