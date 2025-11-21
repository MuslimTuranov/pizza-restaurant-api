**Pizza Restaurant API**

This project includes:

1. CRUD operations for all entities (Restaurant, Pizza, Ingredient, Chef, Review)

2. Relationships between models (One-to-One, One-to-Many, Many-to-Many)

3. Filtering and sorting restaurants by rating

4. Docker + PostgreSQL setup

5. Tests (pytest)

6. Mypy, Ruff, formatting and type checking

Tech Stack:

* FastAPI — backend framework & routing

* SQLAlchemy — ORM

* PostgreSQL — database

* Pydantic — schemas & validation

* Pytest — testing

* Docker + Docker Compose - containerization

* Ruff + Mypy — linting & static type checking


**How to Run with Docker**
```
docker-compose up --build
```

API will be available at:
http://127.0.0.1:8000


Swagger documentation:
http://127.0.0.1:8000/docs


**Running Tests**
```
pytest
```


**Linting**

Ruff
```
ruff check .
ruff format .
```

mypy
```
mypy app/
```

**Request Examples:**
Create a Restaurant
POST /restaurants/
{
  "name": "Dodo Pizza",
  "address": "Rozybakieva 58"
}

Create a Pizza
POST /pizzas/
```
{
  "name": "Pepperoni",
  "cheese_type": "Mozzarella",
  "dough_type": "Thin",
  "secret_ingredient": "Love",
  "restaurant_id": 1,
  "ingredient_ids": [1, 2]
}
```

Update Ingredient
PUT /ingredients/1
```
{
  "name": "Tomato Sauce"
}
```
