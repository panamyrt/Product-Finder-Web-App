# Product Finder Web App

A simple web application built with **Flask** and **MongoDB** that allows users to search, filter, and manage products. The application also includes a basic **content-based recommendation system**.

---

## Features

- Search products by name with filter support
- Add or update products in the database
- Content-based product recommendations using cosine similarity
- Frontend built with HTML, CSS, and JavaScript
- API endpoints for easy integration

---

## Technologies

- **Backend:** Python, Flask
- **Database:** MongoDB
- **Frontend:** HTML, CSS, JavaScript
- **Others:** NumPy

---

## Installation
1. Clone the repository: `git clone https://github.com/panamyrt/Product-Finder-Web-App.git`  
2. Navigate to the folder: `cd Product-Finder-Web-App`  
3. (Optional) Create a virtual environment:  
   - `python -m venv venv`  
   - Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)  
4. Install dependencies: `pip install flask flask-pymongo flask-cors numpy`  
5. Start MongoDB locally at `mongodb://127.0.0.1:27017/pspi`  
6. Run the application: `python app.py`  
7. Open in browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Usage
- Visit the homepage to see products
- Use the search endpoint to filter products
- Add or update products via `/add-product` endpoint
- Get content-based recommendations via `/content-based-filtering` endpoint

## License
Educational purposes only.
