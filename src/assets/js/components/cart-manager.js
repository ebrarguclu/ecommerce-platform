/**
 * Cart Manager Module - PROJ-210
 * Manages shopping cart operations with localStorage
 */

class CartManager {
    constructor() {
        this.STORAGE_KEY = 'ecommerce_cart';
        this.init();
    }

    init() {
        // Initialize cart if not exists
        if (!localStorage.getItem(this.STORAGE_KEY)) {
            this.clearCart();
        }
    }

    // Get cart items
    getCart() {
        const data = localStorage.getItem(this.STORAGE_KEY);
        return data ? JSON.parse(data) : { items: [], total: 0 };
    }

    // Add item to cart
    addItem(product) {
        const cart = this.getCart();
        const existingItem = cart.items.find(item => item.id === product.id);

        if (existingItem) {
            existingItem.quantity += product.quantity || 1;
        } else {
            cart.items.push({
                id: product.id,
                name: product.name,
                price: product.price,
                quantity: product.quantity || 1,
                image: product.image || '',
                addedAt: new Date().toISOString()
            });
        }

        this.updateTotal(cart);
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(cart));
        return { success: true, message: 'Urun sepete eklendi', cart };
    }

    // Remove item from cart
    removeItem(productId) {
        const cart = this.getCart();
        cart.items = cart.items.filter(item => item.id !== productId);
        this.updateTotal(cart);
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(cart));
        return { success: true, message: 'Urun sepetten cikarildi', cart };
    }

    // Update item quantity
    updateQuantity(productId, quantity) {
        const cart = this.getCart();
        const item = cart.items.find(item => item.id === productId);

        if (item) {
            if (quantity <= 0) {
                return this.removeItem(productId);
            }
            item.quantity = quantity;
            this.updateTotal(cart);
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(cart));
            return { success: true, message: 'Miktar guncellendi', cart };
        }

        return { success: false, message: 'Urun bulunamadi' };
    }

    // Calculate total
    updateTotal(cart) {
        cart.subtotal = cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        cart.tax = cart.subtotal * 0.20; // 20% KDV
        cart.shipping = cart.subtotal > 500 ? 0 : 29.99; // 500 TL üzeri ücretsiz kargo
        cart.total = cart.subtotal + cart.tax + cart.shipping;
        return cart;
    }

    // Get cart count
    getItemCount() {
        const cart = this.getCart();
        return cart.items.reduce((sum, item) => sum + item.quantity, 0);
    }

    // Clear cart
    clearCart() {
        const emptyCart = { items: [], subtotal: 0, tax: 0, shipping: 0, total: 0 };
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(emptyCart));
        return { success: true, message: 'Sepet temizlendi', cart: emptyCart };
    }

    // Check if item is in cart
    isInCart(productId) {
        const cart = this.getCart();
        return cart.items.some(item => item.id === productId);
    }
}

// Export for use
const cartManager = new CartManager();
