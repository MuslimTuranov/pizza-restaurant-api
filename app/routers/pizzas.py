from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/pizzas", tags=["Pizzas"])


@router.post("/", response_model=schemas.Pizza)
def create_pizza(data: schemas.PizzaCreate, db: Session = Depends(get_db)):
    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == data.restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant is not found")

    ingredients = (
        db.query(models.Ingredient)
        .filter(models.Ingredient.id.in_(data.ingredient_ids))
        .all()
    )
    if len(ingredients) != len(data.ingredient_ids):
        raise HTTPException(
            status_code=404, detail="One or more ingredients are not found"
        )

    pizza = models.Pizza(
        name=data.name,
        cheese_type=data.cheese_type,
        dough_type=data.dough_type,
        secret_ingredient=data.secret_ingredient,
        restaurant=restaurant,
        ingredients=ingredients,
    )
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    return pizza


@router.get("/", response_model=list[schemas.Pizza])
def list_pizzas(db: Session = Depends(get_db)):
    return db.query(models.Pizza).all()


@router.put("/{pizza_id}", response_model=schemas.Pizza)
def update_pizza(
    pizza_id: int, data: schemas.PizzaUpdate, db: Session = Depends(get_db)
):
    pizza = db.query(models.Pizza).filter(models.Pizza.id == pizza_id).first()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza is not found")

    for field, value in data.dict(exclude={"ingredient_ids"}).items():
        if value is not None:
            setattr(pizza, field, value)

    if data.ingredient_ids:
        ingredients = (
            db.query(models.Ingredient)
            .filter(models.Ingredient.id.in_(data.ingredient_ids))
            .all()
        )
        if len(ingredients) != len(data.ingredient_ids):
            raise HTTPException(
                status_code=404, detail="One or more ingredients are not found"
            )
        pizza.ingredients = ingredients

    db.commit()
    db.refresh(pizza)
    return pizza


@router.delete("/{pizza_id}")
def delete_pizza(pizza_id: int, db: Session = Depends(get_db)):
    pizza = db.query(models.Pizza).filter(models.Pizza.id == pizza_id).first()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza is not found")
    db.delete(pizza)
    db.commit()
    return {"message": "Pizza is deleted"}
