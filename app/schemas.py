# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

# ------------------ Ingredients ------------------

class IngredientBase(BaseModel):
    name: str

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int
    
    class Config:
        from_attributes = True  # Заменяет orm_mode = True в Pydantic v2


class IngredientUpdate(BaseModel):
    name: Optional[str] = None

# ------------------ Pizzas ------------------

class PizzaBase(BaseModel):
    name: str
    cheese_type: str
    dough_type: str
    secret_ingredient: str

class PizzaCreate(PizzaBase):
    restaurant_id: int
    ingredient_ids: List[int] = []

class Pizza(PizzaBase):
    id: int
    
    class Config:
        from_attributes = True


class PizzaUpdate(BaseModel):
    name: Optional[str] = None
    cheese_type: Optional[str] = None
    dough_type: Optional[str] = None
    secret_ingredient: Optional[str] = None

# ------------------ Chefs ------------------

class ChefBase(BaseModel):
    name: str
    restaurant_id: int

class ChefCreate(ChefBase):
    pass

class Chef(ChefBase):
    id: int
    
    class Config:
        from_attributes = True


class ChefUpdate(BaseModel):
    name: Optional[str] = None

# ------------------ Restaurants ------------------

class RestaurantBase(BaseModel):
    name: str
    address: str

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    id: int
    
    class Config:
        from_attributes = True


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

# ------------------ Menu ------------------

class PizzaInMenu(BaseModel):
    name: str
    cheese_type: str
    dough_type: str
    secret_ingredient: str
    ingredients: List[str]
    
    class Config:
        from_attributes = True


class RestaurantMenuResponse(BaseModel):
    restaurant: str
    menu: List[PizzaInMenu]
    
    class Config:
        from_attributes = True

# ------------------ Reviews ------------------

class ReviewBase(BaseModel):
    rating: int
    text: str
    restaurant_id: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    
    class Config:
        from_attributes = True

class ReviewResponse(BaseModel):
    id: int
    rating: int
    text: str
    restaurant_id: int
    restaurant_name: str 
    
    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    text: Optional[str] = None