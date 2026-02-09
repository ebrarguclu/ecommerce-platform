const productController = new ProductController();
let currentProducts = [];

document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
    displayProducts(productController.getAllProducts());
    updateCartCount();
});

function loadCategories() {
    const categoryFilter = document.getElementById('category-filter');
    const categories = productController.getCategories();
    
    categories.forEach(category => {
        if (category !== 'Tumu') {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categoryFilter.appendChild(option);
        }
    });
}

function displayProducts(products) {
    currentProducts = products;
    const container = document.getElementById('products-container');
    const noResults = document.getElementById('no-results');
    
    container.innerHTML = '';
    
    if (products.length === 0) {
        noResults.classList.remove('d-none');
        return;
    }
    
    noResults.classList.add('d-none');
    
    products.forEach(product => {
        const productCard = createProductCard(product);
        container.appendChild(productCard);
    });
}

function createProductCard(product) {
    const col = document.createElement('div');
    col.className = 'col-md-4 col-lg-3 fade-in';
    
    col.innerHTML = `
        <div class="card product-card">
            <img src="${product.image}" class="card-img-top product-image" alt="${product.name}">
            <div class="card-body">
                <span class="badge bg-secondary mb-2">${product.category}</span>
                <h5 class="card-title">${product.name}</h5>
                <p class="card-text text-muted small">${product.description}</p>
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="h5 text-primary mb-0">${product.getFormattedPrice()}</span>
                    <span class="text-warning">
                        <i class="fas fa-star"></i> ${product.rating}
                    </span>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">Stok: ${product.stock}</small>
                    <button class="btn btn-primary btn-sm" onclick="addToCart(${product.id})"
                            ${!product.isAvailable() ? 'disabled' : ''}>
                        <i class="fas fa-cart-plus"></i> Sepete Ekle
                    </button>
                </div>
            </div>
        </div>
    `;
    
    return col;
}

function addToCart(productId) {
    const product = productController.getProductById(productId);
    
    if (!product || !product.isAvailable()) {
        alert('Bu urun stokta yok!');
        return;
    }
    
    StorageManager.addToCart(product);
    updateCartCount();
    showToast('Urun sepete eklendi!', 'success');
}

function searchProducts() {
    const query = document.getElementById('search-input').value;
    const products = productController.searchProducts(query);
    displayProducts(products);
}

function filterByCategory() {
    const category = document.getElementById('category-filter').value;
    const products = productController.getProductsByCategory(category);
    displayProducts(products);
}

function updateCartCount() {
    const cart = StorageManager.getCart();
    const cartCount = document.getElementById('cart-count');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
}

function showToast(message, type = 'info') {
    const alertClass = type === 'success' ? 'success' : 'info';
    const toast = document.createElement('div');
    toast.className = `alert alert-${alertClass} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

document.getElementById('search-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchProducts();
    }
});
