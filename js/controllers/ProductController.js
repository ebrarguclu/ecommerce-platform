class ProductController {
    constructor() {
        this.products = this.initializeProducts();
    }

    initializeProducts() {
        return [
            new Product(1, 'iPhone 15 Pro', 45999, 'Elektronik', 'Apple iPhone 15 Pro 256GB', 'https://via.placeholder.com/300x300/0d6efd/ffffff?text=iPhone+15+Pro', 15),
            new Product(2, 'Samsung Galaxy S24', 39999, 'Elektronik', 'Samsung Galaxy S24 Ultra 512GB', 'https://via.placeholder.com/300x300/0d6efd/ffffff?text=Galaxy+S24', 12),
            new Product(3, 'MacBook Pro M3', 89999, 'Elektronik', 'Apple MacBook Pro 16" M3 Max', 'https://via.placeholder.com/300x300/0d6efd/ffffff?text=MacBook+Pro', 8),
            new Product(4, 'Sony WH-1000XM5', 9999, 'Elektronik', 'Sony Kablosuz Kulaklik', 'https://via.placeholder.com/300x300/0d6efd/ffffff?text=Sony+WH1000XM5', 20),
            new Product(5, 'Erkek Kot Pantolon', 299, 'Giyim', 'Slim Fit Erkek Kot Pantolon', 'https://via.placeholder.com/300x300/6c757d/ffffff?text=Kot+Pantolon', 50),
            new Product(6, 'Kadin Elbise', 499, 'Giyim', 'Sik Kadin Elbise - Cicek Desenli', 'https://via.placeholder.com/300x300/6c757d/ffffff?text=Elbise', 30),
            new Product(7, 'Spor Ayakkabi', 899, 'Giyim', 'Erkek Kosu Ayakkabisi', 'https://via.placeholder.com/300x300/6c757d/ffffff?text=Ayakkabi', 40),
            new Product(8, 'Koltuk Takimi', 15999, 'Ev & Yasam', 'Modern 3+2+1 Koltuk Takimi', 'https://via.placeholder.com/300x300/198754/ffffff?text=Koltuk', 5),
            new Product(9, 'LED TV 55"', 12999, 'Elektronik', 'Samsung 55" 4K Smart LED TV', 'https://via.placeholder.com/300x300/0d6efd/ffffff?text=LED+TV', 10),
            new Product(10, 'Kahve Makinesi', 1299, 'Ev & Yasam', 'Otomatik Kahve Makinesi', 'https://via.placeholder.com/300x300/198754/ffffff?text=Kahve', 25),
        ];
    }

    getAllProducts() {
        return this.products;
    }

    getProductById(id) {
        return this.products.find(p => p.id === parseInt(id));
    }

    getProductsByCategory(category) {
        if (category === 'Tumu') return this.products;
        return this.products.filter(p => p.category === category);
    }

    searchProducts(query) {
        const lowerQuery = query.toLowerCase();
        return this.products.filter(p => 
            p.name.toLowerCase().includes(lowerQuery) ||
            p.description.toLowerCase().includes(lowerQuery)
        );
    }

    getCategories() {
        const categories = ['Tumu', ...new Set(this.products.map(p => p.category))];
        return categories;
    }
}
