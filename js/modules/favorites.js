/**
 * Favorites Module - PROJ-205
 * Manages user favorite products with localStorage
 */

class FavoritesManager {
    constructor() {
        this.STORAGE_KEY = 'ecommerce_favorites';
    }

    // Get all favorites
    getFavorites() {
        const data = localStorage.getItem(this.STORAGE_KEY);
        return data ? JSON.parse(data) : [];
    }

    // Add to favorites
    addFavorite(productId, productName, productPrice) {
        const favorites = this.getFavorites();
        
        // Check if already exists
        if (favorites.some(item => item.id === productId)) {
            return { success: false, message: 'Urun zaten favorilerde' };
        }

        favorites.push({
            id: productId,
            name: productName,
            price: productPrice,
            addedAt: new Date().toISOString()
        });

        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(favorites));
        return { success: true, message: 'Favorilere eklendi' };
    }

    // Remove from favorites
    removeFavorite(productId) {
        let favorites = this.getFavorites();
        favorites = favorites.filter(item => item.id !== productId);
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(favorites));
        return { success: true, message: 'Favorilerden cikarildi' };
    }

    // Check if product is favorite
    isFavorite(productId) {
        return this.getFavorites().some(item => item.id === productId);
    }

    // Get favorites count
    getCount() {
        return this.getFavorites().length;
    }

    // Clear all favorites
    clearAll() {
        localStorage.removeItem(this.STORAGE_KEY);
        return { success: true, message: 'Tum favoriler temizlendi' };
    }
}

// Export for use
const favoritesManager = new FavoritesManager();
