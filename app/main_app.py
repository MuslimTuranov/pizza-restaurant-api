from fastapi import FastAPI
from app.database import Base, engine
from app.routers import restaurants, pizzas, chefs, reviews, ingredients

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pizza Restaurant API",
    description="API для управления пиццериями",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Pizza Restaurant API is running",
        "status": "ok",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "Pizza API"}

app.include_router(restaurants.router)
app.include_router(pizzas.router)
app.include_router(chefs.router)
app.include_router(ingredients.router)
app.include_router(reviews.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    

# docker-compose logs api --tail=20

