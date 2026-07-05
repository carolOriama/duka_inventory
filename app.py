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


if __name__=="__main__":
    app.run(debug=True)
