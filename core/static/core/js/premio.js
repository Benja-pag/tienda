document.addEventListener("DOMContentLoaded", function() {
  const productContainer = document.getElementById('product-container');
  
  fetch('https://fakestoreapi.com/products')
      .then(response => response.json())
      .then(products => {
          products.forEach(product => {
              const productCard = `
                  <div class="col-md-4 mb-4">
                      <div class="card h-100">
                          <img class="card-img-top" src="${product.image}" alt="Product Image">
                          <div class="card-body">
                              <h5 class="card-title">${product.title}</h5>
                              <p class="card-text">${product.description.substring(0, 100)}...</p>
                              <p class="card-price">Price: $${product.price}</p>
                              <a href="#" class="btn btn-primary">Add to Cart</a>
                          </div>
                      </div>
                  </div>
              `;
              productContainer.innerHTML += productCard;
          });
      })
      .catch(error => console.error('Error fetching the products:', error));
});