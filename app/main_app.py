from fastapi import FastAPI
from app.database import Base, engine
from app.routers import restaurants, pizzas, chefs, reviews, ingredients

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(restaurants.router)
app.include_router(pizzas.router)
app.include_router(chefs.router)
app.include_router(ingredients.router)
app.include_router(reviews.router)
