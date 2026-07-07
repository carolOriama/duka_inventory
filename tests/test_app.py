import pytest
from unittest.mock import patch, Mock
from app import app, products

@pytest.fixture
def client():
    
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_database():
    products.clear()
    products[1] = {
        "id": 1,
        "barcode": "025293001225",
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "ingredients": "Filtered water, almonds, cane sugar...",
        "price": 3.99,
        "quantity": 50
    }

def test_get_all_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["product_name"] == "Organic Almond Milk"

def test_get_single_product_success(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["brand"] == "Silk"

def test_get_single_product_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    
    data = response.get_json()
    assert "error" in data

@patch("app.requests.get")
def test_create_product_success(mock_get, client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Mock Peanut Butter",
            "brands": "Test Brand",
            "ingredients_text": "Peanuts, Salt."
        }
    }
    mock_get.return_value = mock_response

    payload = {"barcode": "11111111", "price": 2.50, "quantity": 10}
    response = client.post("/inventory", json=payload)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 2
    assert data["product_name"] == "Mock Peanut Butter"
    assert products[2]["price"] == 2.50
