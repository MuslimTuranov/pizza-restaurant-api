from fastapi.testclient import TestClient
from .main_app import app

client = TestClient(app)

def test_create_pizza():
    response = client.post(
        "/pizzas/",
        json={
            "name": "Pepperoni",
            "cheese_type": "Mozzarella",
            "dough_type": "Thin Crust",
            "secret_ingredient": "Basil Oil",
            "restaurant_id": 1,
            "ingredient_ids": [1, 2]
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Pepperoni"
    assert data["cheese_type"] == "Mozzarella"
    assert data["dough_type"] == "Thin Crust"
    assert data["secret_ingredient"] == "Basil Oil"
    assert data["ingredients"] == [
        {"id": 1, "name": "Tomato"},
        {"id": 2, "name": "Sausage"}
    ]



def test_create_bad_pizza():
    response = client.post(
        "/pizzas/",
        json={
            "name": "Pepperoni",
            "cheese_type": "Mozzarella",
            "dough_type": "Thin Crust",
            "secret_ingredient": "Basil Oil",
            "restaurant_id": 2,
            "ingredient_ids": [1, 2]
        }
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant not found"}