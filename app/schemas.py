from pydantic import BaseModel
from typing import List, Optional


class IngredientBase(BaseModel):
    name: str


class IngredientCreate(IngredientBase):
    class Config:
        orm_mode = True


class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True


class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    pizza_ids: List[int] = []

    class Config:
        orm_mode = True


class PizzaBase(BaseModel):
    name: str
    cheese_type: str
    dough_type: str
    secret_ingredient: str


class PizzaCreate(PizzaBase):
    restaurant_id: int
    ingredient_ids: List[int] = []

    class Config:
        orm_mode = True


class PizzaUpdate(BaseModel):
    name: Optional[str] = None
    cheese_type: Optional[str] = None
    dough_type: Optional[str] = None
    secret_ingredient: Optional[str] = None
    ingredient_ids: List[int] = []

    class Config:
        orm_mode = True


class Pizza(PizzaBase):
    id: int
    ingredients: List[Ingredient] = []

    class Config:
        orm_mode = True


class ChefBase(BaseModel):
    name: str
    restaurant_id: int


class ChefCreate(ChefBase):
    class Config:
        orm_mode = True


class Chef(ChefBase):
    id: int

    class Config:
        orm_mode = True


class ChefUpdate(BaseModel):
    name: Optional[str] = None
    restaurant_id: Optional[int] = None

    class Config:
        orm_mode = True


class RestaurantBase(BaseModel):
    name: str
    address: str


class RestaurantCreate(RestaurantBase):
    class Config:
        orm_mode = True


class Restaurant(RestaurantBase):
    id: int
    chef: Optional[Chef] = None
    pizzas: List[Pizza] = []

    class Config:
        orm_mode = True


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    chef_id: Optional[int] = None
    pizza_ids: List[int] = []

    class Config:
        orm_mode = True


class PizzaInMenu(BaseModel):
    name: str
    cheese_type: str
    dough_type: str
    secret_ingredient: str
    ingredients: List[str]


class RestaurantMenuResponse(BaseModel):
    restaurant: str
    menu: List[PizzaInMenu]


class ReviewBase(BaseModel):
    rating: int
    text: str
    restaurant_id: int

    class Config:
        orm_mode = True


class ReviewResponse(BaseModel):
    id: int
    rating: int
    text: str
    restaurant_id: int
    restaurant_name: str

    class Config:
        orm_mode = True


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
    pizza_id: Optional[int] = None

    class Config:
        orm_mode = True
