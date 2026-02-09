function displayProducts(productsArray) {
    const container = document.getElementById('product-grid');
    if(!container) return;
    container.innerHTML = ''; 
    productsArray.forEach(product => {
        const card = `
            <div class="product-card">
                <img src="${product.image}" alt="${product.name}">
                <div class="card-content">
                    <h3>${product.name}</h3>
                    <p class="price">$${product.price}</p>
                    <button class="btn-add" onclick="handleAddToCart(${product.id})">Add to Cart</button>
                </div>
            </div>`;
        container.innerHTML += card;
    });
}
function handleAddToCart(id) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const product = productDatabase.find(p => p.id === id);
    cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));
    alert(product.name + " added to cart!");
}
displayProducts(productDatabase);
