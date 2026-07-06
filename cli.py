import requests

BASE_URL = "http://127.0.0.1:5000/inventory"

def display_menu():
    print("1. View Full Inventory")
    print("2. Search Item by ID")
    print("3. Add New Item (via Barcode)")
    print("4. Update Stock or Price (PATCH)")
    print("5. Delete Item from System")
    print("6. Exit Portal")

def get_all_items():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            items = response.json()
            if not items:
                print("\n[!] The inventory is currently empty.")
                return
            
            print(f"\n{'ID':<5} | {'Product Name':<30} | {'Brand':<15} | {'Price':<8} | {'Stock':<6}")
            print("-" * 75)
            for item in items:
                print(f"{item['id']:<5} | {item['product_name'][:30]:<30} | {item['brand'][:15]:<15} | ${item['price']:<7.2f} | {item['quantity']:<6}")
        else:
            print(f"\n[Error] Server returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("\n[Error] Unable to reach the API server. Is app.py running?")

def add_item():
    print("\n--- Add New Inventory Item ---")
    barcode = input("Scan/Enter Barcode: ").strip()
    try:
        price = float(input("Enter Selling Price: $"))
        quantity = int(input("Enter Initial Stock Level: "))
    except ValueError:
        print("[Error] Invalid numeric format entered for price or quantity.")
        return

    payload = {"barcode": barcode, "price": price, "quantity": quantity}
    
    print("Querying OpenFoodFacts... please wait...")
    try:
        response = requests.post(BASE_URL, json=payload)
        if response.status_code == 201:
            data = response.json()
            print(f"\n[Success] Added: {data['product_name']} ({data['brand']}) successfully integrated.")
        else:
            # Displays the custom error message we wrote in app.py (e.g., product not found)
            print(f"\n[Error] {response.json().get('error', 'Failed to add item.')}")
    except requests.exceptions.ConnectionError:
        print("\n[Error] Server is down.")

def update_item():
    print("\n--- Update Existing Item ---")
    try:
        item_id = int(input("Enter the ID of the item to update: "))
    except ValueError:
        print("[Error] ID must be an integer.")
        return

    print("Leave field blank and hit Enter if you don't want to change it.")
    price_input = input("Enter new price (or skip): $").strip()
    qty_input = input("Enter new stock level (or skip): ").strip()

    payload = {}
    if price_input:
        payload["price"] = float(price_input)
    if qty_input:
        payload["quantity"] = int(qty_input)

    if not payload:
        print("[!] No update modifications specified.")
        return

    try:
        response = requests.patch(f"{BASE_URL}/{item_id}", json=payload)
        if response.status_code == 200:
            print("\n[Success] Item metrics updated changes saved.")
        else:
            print(f"\n[Error] {response.json().get('error', 'Item not found.')}")
    except requests.exceptions.ConnectionError:
        print("\n[Error] Server is down.")

def delete_item():
    print("\n--- Remove Item From Inventory ---")
    try:
        item_id = int(input("Enter the ID of the item to delete: "))
    except ValueError:
        print("[Error] ID must be an integer.")
        return

    confirm = input(f"Are you sure you want to permanently delete item #{item_id}? (y/N): ").lower()
    if confirm != 'y':
        print("[!] Operation canceled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/{item_id}")
        if response.status_code == 200:
            print(f"\n[Success] {response.json().get('message')}")
        else:
            print(f"\n[Error] {response.json().get('error', 'Failed to delete item.')}")
    except requests.exceptions.ConnectionError:
        print("\n[Error] Server is down.")

def main():
    while True:
        display_menu()
        choice = input("Select an administration task (1-6): ").strip()
        
        if choice == "1":
            get_all_items()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            print("\nExiting Admin Portal. Goodbye!")
            break
        else:
            print("\n[!] Invalid choice. Please pick an option between 1 and 6.")

if __name__ == "__main__":
    main()