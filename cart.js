let cart = [];

function addItemToCart(itemName) {
    // Find the item element by name
    const itemElement = document.querySelector(`.item[data-name="${itemName}"]`);
    
    if (!itemElement) {
        console.error('Item not found:', itemName);
        return;
    }

    // Read the price from the data attribute
    const itemPrice = parseFloat(itemElement.getAttribute('data-price'));

    const item = {
        name: itemName,
        price: itemPrice,
        quantity: 1
    };

    const existingItem = cart.find(cartItem => cartItem.name === itemName);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push(item);
    }

    updateCartDisplay();
}

function updateCartDisplay() {
    const cartItemsContainer = document.getElementById('cart-items');
    cartItemsContainer.innerHTML = '';

    let total = 0;

    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - $${item.price.toFixed(2)} x ${item.quantity}`;
        cartItemsContainer.appendChild(li);
        total += item.price * item.quantity;
    });

    document.getElementById('cart-total').textContent = `Subtotal: $${total.toFixed(2)}`;
}
