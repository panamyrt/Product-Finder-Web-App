# BEGIN CODE HERE
from flask import Flask, jsonify, request, make_response,send_file, redirect, url_for
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
import json
import numpy as np
from numpy.linalg import norm
import uuid
# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"

mongo = PyMongo(app)


@app.route('/')
def home():
   return send_file('homepage.html')

@app.route('/products')
def products():
    return send_file('products.html')
    
    
@app.route('/homepage.html')
def redirect_to_homepage():
    return send_file('homepage.html')

@app.route('/products.html')
def redirect_to_products_page():
    return redirect(url_for('products'))
    
        
@app.route('/logo.png')
def logo():
    return send_file('logo.png')
    
@app.route('/image-1.jpg')
def image1():
    return send_file("image-1.jpg")
    
@app.route('/image-2.jpg')
def image2():
    return send_file('image-2.jpg')
 
@app.route('/image-3.jpg')
def image3():
    return send_file('image-3.jpg')
    
@app.route('/products.css')
def products_css():
    return send_file('products.css')
 
@app.route('/products.js')
def products_js():
    return send_file('products.js')
     
@app.route('/homepage.css')
def homepage_css():
    return send_file('homepage.css')




@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Name parameter is required"}), 400

    try:
        # Χρήση regex για μερική αναζήτηση και ταξινόμηση κατά φθίνουσα σειρά της τιμής
        results = mongo.db.products.find({"name": {"$regex": name, "$options": "i"}}).sort("price", -1)
        products = []
        for result in results:
            product = {
                "id": result.get("id"),
                "name": result.get("name"),
                "production_year": result.get("production_year"),
                "price": result.get("price"),
                "color": result.get("color"),
                "size": result.get("size")
            }
            products.append(product)
        
        response = make_response(json.dumps(products, ensure_ascii=False))
        response.mimetype = 'application/json'
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    new_product = request.json
    
    if not new_product:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        # Έλεγχος αν το πεδίο "Name" υπάρχει στο JSON
        if "name" not in new_product:
            return jsonify({"error": "Missing field: Name"}), 400
        
        # Έλεγχος αν το πεδίο "color" περιέχει έναν έγκυρο κωδικό
        valid_colors = [1, 2, 3]
        if "color" in new_product and new_product["color"] not in valid_colors:
            return jsonify({"error": "Invalid color code"}), 400
        
        # Έλεγχος αν το πεδίο "size" περιέχει έναν έγκυρο κωδικό
        valid_sizes = [1, 2, 3, 4]
        if "size" in new_product and new_product["size"] not in valid_sizes:
            return jsonify({"error": "Invalid size code"}), 400

        exists = mongo.db.products.find_one({"name": new_product["name"]})
        if exists:
            # Διαγραφή υπάρχοντος εγγράφου
            mongo.db.products.delete_one({"name": new_product["name"]})

        # Προσθήκη νέου εγγράφου
        new_product["id"] = str(uuid.uuid4())

        mongo.db.products.insert_one(new_product)
        return jsonify({"message": "Document added!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # Λάβετε τα δεδομένα του νέου προϊόντος από το request
    new_product = request.json
    
    # Ελέγξτε αν τα δεδομένα που λήφθηκαν είναι έγκυρα
    if not new_product or not all(key in new_product for key in ("name", "production_year", "price", "color", "size")):
        return jsonify({"error": "Invalid input format"}), 400

    # Λάβετε όλα τα προϊόντα από τη βάση δεδομένων
    products = mongo.db.products.find()
    
    # Δημιουργία ενός κενού λεξικού για να αποθηκεύσετε τα ονόματα των προϊόντων που έχουν ομοιότητα μεγαλύτερη από 70%
    similar_products = []

    # Δημιουργία ενός διανύσματος από τα δεδομένα του νέου προϊόντος
    new_product_vector = np.array([
        new_product["production_year"],
        new_product["price"],
        new_product["color"],
        new_product["size"]
    ], dtype=np.float64)

    for product in products:
        # Δημιουργία ενός διανύσματος από τα δεδομένα του κάθε προϊόντος
        product_vector = np.array([
            product["production_year"],
            product["price"],
            product["color"],
            product["size"]
        ], dtype=np.float64)

        # Υπολογισμός της ομοιότητας χρησιμοποιώντας την cosine similarity
        cos_sim = np.dot(product_vector, new_product_vector) / (norm(product_vector) * norm(new_product_vector))

        # Αν η ομοιότητα είναι μεγαλύτερη από 0.7, προσθέστε το όνομα του προϊόντος στη λίστα
        if cos_sim > 0.7:
            similar_products.append(product["name"])

    # Επιστροφή των ονομάτων των προϊόντων που έχουν ομοιότητα μεγαλύτερη από 70%
    return jsonify(similar_products)
    
    
    
    
@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE
    

if __name__ == '__main__':
    app.run(debug=True)