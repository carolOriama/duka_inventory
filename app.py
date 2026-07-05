from flask import Flask, jsonify
import requests

app = Flask(__name__)


def fetch_product(barcode):

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    try:
        #Add header so that api knows who is calling it.
        headers = {'User-Agent': 'InventoryManagerApp - WebCourseProject - Version 1.0'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == 1:
                product_info = data.get("product", {})
                
                return {
                    "product_name": product_info.get("product_name", "None"),
                    "brand": product_info.get("brands", "None"),
                    "ingredients": product_info.get("ingredients_text", "None.")
                }
    except requests.exceptions.RequestException as e:
        print(f"External API Error: {e}")


    return None

products = [
         {
        "id": 1,
        "barcode": "025293001225",
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "ingredients": "Filtered water, almonds, cane sugar...",
        "price": 3.99,
        "quantity": 50
    }
]


"""Implementing CRUD"""

@app.route("/inventory", methods=["GET"])
def get_all_products():
    return jsonify(list(products.values())),200

@app.route("/inventory/<int:id>", methods = ["GET"])
def get_product(id):
    product = products.get(id)
    if product:
        return jsonify(product), 200
    return jsonify({"Product not found"}), 404

@app.route("/inventory", methods= ["POST"])
def create_product(id):
    data = request.get_json()
    if not data or "barcode" not in data or "price" not in data or "quantity" not in data:
        return jsonify({"error": "Missing required fields: barcode, price, quantity"}), 400
    
    barcode = data["barcode"]

    external_data = fetch_product(barcode)
    if not external_data:
        return jsonify({"error": f"Product with barcode {barcode} could not be found on OpenFoodFacts."}), 422
    
    new_id = max(products.keys()) + 1 if products else 1

    new_item = {
        "id": new_id,
        "barcode": barcode,
        "product_name": external_data["product_name"],
        "brand": external_data["brand"],
        "ingredients": external_data["ingredients"],
        "price": float(data["price"]),
        "quantity": int(data["quantity"])
    }

    products[new_id] = new_item
    return jsonify(new_item), 201

@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
    item = products.get(id)
    if not item:
        return jsonify({"Item not found"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"No data provided"}), 400

    if "price" in data:
        item["price"] = float(data["price"])
    if "quantity" in data:
        item["quantity"] = int(data["quantity"])
        
    return jsonify(item), 200


@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
    global products
    if id in products:
        del products[id]
        return jsonify({"message": f"Item {id} successfully deleted"}), 200
    return jsonify({"Item not found"}), 404


if __name__=="__main__":
    app.run(debug=True, port=5000)
