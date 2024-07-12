
document.addEventListener('DOMContentLoaded', function() {

    fetch('http://fakestoreapi.com/products')
        .then(response => response.json()) 
        .then(data => {

            const productContainer = document.getElementById('product-container');


            productContainer.innerHTML = '';


            data.forEach(item => {
                
                const cardHTML = `
                    <div class="col-sm-12 col-md-6 col-lg-4 col-xl-4 mb-3 text-center">
                        <div class="card h-100" style="width: 100%;">
                            <img src="${item.image}" class="card-img-top pt-3" style="width: 475px; height: 555px; object-fit: cover; margin: auto;">
                            <div class="card-body">
                                <h5 class="card-title">${item.title}</h5>
                                <h6>${item.category}</h6>
                                <p class="card-text">${item.description.substring(0, 100)}...</p>
                                <p class="card-price">Price: $${item.price}</p>
                                <a class="btn btn-primary" target="_blank" href="https://www.amazon.com/s?k=${item.title}">Comprar</a>
                            </div>
                        </div>
                    </div>
                `;

                productContainer.innerHTML += cardHTML;
            });

        })
        .catch(error => console.error('Error al obtener los datos:', error));

});
