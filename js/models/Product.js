class Product {
    constructor(id, name, price, category, description, image, stock = 10) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.category = category;
        this.description = description;
        this.image = image;
        this.stock = stock;
        this.rating = 4.5;
        this.reviews = Math.floor(Math.random() * 100) + 10;
    }

    isAvailable() {
        return this.stock > 0;
    }

    getFormattedPrice() {
        return `${this.price.toLocaleString('tr-TR')} TL`;
    }

    decreaseStock(quantity = 1) {
        if (this.stock >= quantity) {
            this.stock -= quantity;
            return true;
        }
        return false;
    }
}
