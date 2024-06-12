function Enter(event) {
    if (event.key === 'Enter') {
        filterProducts();
    }
}

function filterProducts() {
    var input, filter, products, product, title, i;
    input = document.getElementById("search-input");
    filter = input.value.toLowerCase();
    products = document.getElementsByClassName("product");

    for (i = 0; i < products.length; i++) {
        product = products[i];
        title = product.getElementsByClassName("product-title")[0];
        if (title.innerHTML.toLowerCase().indexOf(filter) > -1) {
            product.style.display = "";
        } else {
            product.style.display = "none";
        }
    }
}
document.addEventListener('DOMContentLoaded', () => {
    const types = document.querySelectorAll('.type');
    const products = document.querySelectorAll('.product');

    types.forEach(type => {
        type.addEventListener('mouseenter', () => {
            const category = type.getAttribute('data-category');
            products.forEach(product => {
                if (product.getAttribute('data-category') === category) {
                    product.style.display = 'block';
                } else {
                    product.style.display = 'none';
                }
            });
        });      
            });
        });

