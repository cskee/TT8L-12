let previewContainer = document.querySelector('.product-preview');
let previewBox = previewContainer.querySelectorAll('.preview');

document.querySelectorAll('.product-container1 .product').forEach(product =>{
  product.onclick = () =>{
    previewContainer.style.display = 'flex';
    let name = product.getAttribute('data-name');
    previewBox.forEach(preview =>{
      let target = preview.getAttribute('data-target');
      if(name == target){
        preview.classList.add('active');
      }
    });
  };
});

document.getElementById('sorting').addEventListener('change', function() {
  let container = document.getElementById('productContainer');
  let products = Array.from(container.getElementsByClassName('product'));
  let sortValue = this.value;

  if (sortValue === 'lowToHigh') {
      products.sort((a, b) => {
          let priceA = parseFloat(a.querySelector('.discounted-price').textContent.replace('RM', ''));
          let priceB = parseFloat(b.querySelector('.discounted-price').textContent.replace('RM', ''));
          return priceA - priceB;
      });
  } else if (sortValue === 'highToLow') {
      products.sort((a, b) => {
          let priceA = parseFloat(a.querySelector('.discounted-price').textContent.replace('RM', ''));
          let priceB = parseFloat(b.querySelector('.discounted-price').textContent.replace('RM', ''));
          return priceB - priceA;
      });
  } else {
  }

  container.innerHTML = '';
  products.forEach(product => container.appendChild(product));
});

previewBox.forEach(close =>{
  close.querySelector('.fa-times').onclick = () =>{
    close.classList.remove('active');
    previewContainer.style.display = 'none';
  };
});