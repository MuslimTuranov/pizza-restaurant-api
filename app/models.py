from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

pizza_ingredient = Table(
    "pizza_ingredient",
    Base.metadata,
    Column("pizza_id", ForeignKey("pizzas.id"), primary_key=True),
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True),
)

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    address = Column(String)
    chef = relationship("Chef", back_populates="restaurant", uselist=False)
    pizzas = relationship("Pizza", back_populates="restaurant")
    reviews = relationship("Review", back_populates="restaurant")

class Chef(Base):
    __tablename__ = "chefs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="chef")

class Pizza(Base):
    __tablename__ = "pizzas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cheese_type = Column(String)
    dough_type = Column(String)
    secret_ingredient = Column(String)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="pizzas")
    ingredients = relationship(
        "Ingredient", secondary=pizza_ingredient, back_populates="pizzas"
    )

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    pizzas = relationship(
        "Pizza", secondary=pizza_ingredient, back_populates="ingredients"
    )

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    rating = Column(Integer)
    text = Column(String)
    restaurant = relationship("Restaurant", back_populates="reviews")