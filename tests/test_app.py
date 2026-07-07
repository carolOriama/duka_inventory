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
