const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    const searchButton = document.getElementById('search');
    const saveButton = document.getElementById('save');
    
    if (searchButton) {
        searchButton.addEventListener('click', searchButtonOnClick);
    } else {
        console.error('Search button not found');
    }

    if (saveButton) {
        saveButton.addEventListener('click', productFormOnSubmit);
    } else {
        console.error('Save button not found');
    }
    // END CODE HERE
}

const searchButtonOnClick = (event) => {
    event.preventDefault();
    const productName = document.getElementById('searchInput').value; // Παίρνουμε την τιμή από το input
    fetch(`${api}/search?name=${encodeURIComponent(productName)}`) // Χρησιμοποιούμε την τιμή για να κάνουμε το request
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const tbody = document.getElementById('productTableBody');
        tbody.innerHTML = '';
        data.forEach(product => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.production_year}</td>
                <td>${product.price}</td>
                <td>${product.color}</td>
                <td>${product.size}</td>
            `;
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


const productFormOnSubmit = (event) => {
    // BEGIN CODE HERE
    event.preventDefault();

    const name = document.getElementById('name').value;
    const pyear = document.getElementById('pyear').value;
    const price = document.getElementById('price').value;
    const color = document.getElementById('color').value;
    const size = document.getElementById('size').value;

    const productData = {
        name: name,
        production_year: parseInt(pyear),
        price: parseFloat(price),
        color: parseInt(color),
        size: parseInt(size)
    };

    console.log('Product data to be submitted:', productData);

    fetch(`${api}/add-product`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Product added:', data);
        alert('Product added or updated successfully! ID: ' + data._id);
        document.getElementById('name').value = '';
        document.getElementById('pyear').value = '';
        document.getElementById('price').value = '';
        document.getElementById('color').value = '';
        document.getElementById('size').value = '';
    })
    .catch(error => {
        console.error('Error:', error);
    });
    // END CODE HERE
}

