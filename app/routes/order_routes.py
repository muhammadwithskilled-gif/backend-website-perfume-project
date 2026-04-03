from flask import Blueprint, jsonify, request, send_from_directory
from pathlib import Path
from app.utils.json_db import get_product, get_all_products
from app.utils.google_sheet import save_order_to_sheet
from app import config

order_bp = Blueprint("order", __name__)

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# ------------------------------
# Route 1: Home Page
# ------------------------------
@order_bp.route("/")
def home():
    return jsonify({
        "message": "Welcome to Perfume & Watches Store"
    })

# ------------------------------
# Route 2: Get All Products
# ------------------------------
@order_bp.route("/products", methods=["GET"])
def all_products():
    products = get_all_products()
    
    if not products:
        return jsonify([])
    
    return jsonify(products)

# ------------------------------
# Route 3: Get Single Product
# ------------------------------
@order_bp.route("/product/<product_id>", methods=["GET"])
def product_detail(product_id):
    product = get_product(product_id)
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    response = {
        "id": product.get("id"),
        "name": product.get("name"),
        "category": product.get("category"),
        "gender": product.get("gender"),
        "price": product.get("price"),
        "availability": product.get("availability"),
        "fragrance_lasting": product.get("fragrance_lasting"),
        "bottle_size": product.get("bottle_size"),
        "description": product.get("description"),
        "features": product.get("features", []),
        "images": product.get("images", [])
    }
    
    return jsonify(response)


# ------------------------------
# Route 4: Serve Images from Database
# ------------------------------

@order_bp.route('/database/<path:filename>')
def serve_database_image(filename):
    try:
        database_path = PROJECT_ROOT / "database"
        return send_from_directory(database_path, filename)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": "Image not found"}), 404

# ------------------------------
# Route 5: Place Order
# ------------------------------
@order_bp.route("/order/<product_id>", methods=["POST"])
def place_order(product_id):
    product = get_product(product_id)
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.json
    
    # -------- Validation --------
    if len(data.get("name", "")) > config.MAX_NAME_LENGTH:
        return jsonify({"error": "Name too long"}), 400
    
    if len(data.get("address", "")) > config.MAX_ADDRESS_LENGTH:
        return jsonify({"error": "Address too long"}), 400
    
    mobile = data.get("mobile", "")
    if not mobile.isdigit() or len(mobile) > config.MAX_MOBILE_LENGTH:
        return jsonify({"error": "Invalid mobile number"}), 400
    
    # -------- Extract Product Data Safely --------
    price_data = product.get("price", {})
    product_price = price_data.get("discounted") or price_data.get("original")
    
    # -------- Create Order Object --------
    order_data = {
        "product_name": product.get("name", ""),
        "product_detail": product.get("category", ""),
        "product_description": product.get("description", ""),
        "delivery_time": "3-5 days",
        "payment_method": data.get("payment_method", "COD"),
        "customer_name": data.get("name", ""),
        "customer_address": data.get("address", ""),
        "delivery_date": data.get("delivery_date", ""),
        "status": "Pending"
    }
    
    # -------- Save to Google Sheet --------
    save_order_to_sheet(order_data)
    
    return jsonify({
        "message": "Order placed successfully",
        "product": product.get("name"),
        "price": product_price
    })