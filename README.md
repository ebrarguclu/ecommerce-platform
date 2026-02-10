# E-Commerce Platform

Modern, responsive e-commerce web application with shopping cart, product catalog, and order management.

## Features

- Product catalog with search and filtering
- Shopping cart management
- User authentication and profiles
- Order tracking
- Payment integration ready
- Fully responsive design

## Technologies

- HTML5, CSS3, JavaScript (ES6+)
- Bootstrap 5 for UI
- LocalStorage for data persistence
- RESTful API structure

## Installation
```bash
# Clone the repository
git clone https://github.com/ebrarguclu/ecommerce-platform.git

# Open index.html in browser
# Or use live server
```

## Usage

1. Browse products in the catalog
2. Add items to cart
3. Manage cart quantities
4. Complete checkout process
5. View order history

## Contributing

We follow GitFlow workflow. See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## License

MIT License

## Version 1.1.0 Features

### New Pages
- **User Profile Management** - Kullanici profil bilgileri yonetimi
- **Order History** - Siparis gecmisi ve takip sistemi
- **Product Comparison** - Urunleri karsilastirma ozelligi

### New Modules
- **Favorites Manager** - localStorage tabanli favori urunler yonetimi
- **Enhanced User Experience** - Gelismis kullanici deneyimi

### Improvements
- Better navigation structure
- Responsive design enhancements
- Modern UI components with Bootstrap 5
- Font Awesome icons integration

### Technical Details
- PROJ-203: User profile page implementation
- PROJ-204: Order history tracking system
- PROJ-205: Favorites management module
- PROJ-206: Product comparison feature

## Version 1.2.0 Features

### New Pages
- **Shopping Cart** - Sepet yonetimi ve odeme sureci
- **Wishlist** - Istek listesi ve favori urunler

### New Modules
- **Cart Manager** - localStorage tabanli sepet yonetim sistemi
  - Urun ekleme/cikarma
  - Miktar guncelleme
  - Otomatik toplam hesaplama
  - KDV ve kargo hesaplama
  - Ucretsiz kargo (500 TL uzeri)

### Improvements
- Enhanced shopping experience
- Real-time cart updates
- Stock status indicators
- Product rating display
- Responsive cart design

### Technical Details
- PROJ-208: Shopping cart page implementation
- PROJ-209: Wishlist page with stock management
- PROJ-210: Cart manager module with localStorage
- PROJ-211: Documentation updates for v1.2.0

### Cart Manager API
```javascript
// Add product to cart
cartManager.addItem({
    id: 1,
    name: 'iPhone 15 Pro',
    price: 52999,
    quantity: 1
});

// Get cart items
const cart = cartManager.getCart();

// Update quantity
cartManager.updateQuantity(1, 2);

// Remove item
cartManager.removeItem(1);

// Clear cart
cartManager.clearCart();
```
