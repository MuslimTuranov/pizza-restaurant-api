from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.post("/", response_model=schemas.Ingredient)
def create_ingredient(data: schemas.IngredientCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(models.Ingredient).filter(models.Ingredient.name == data.name).first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Ingredient already exists")

    ingredient = models.Ingredient(name=data.name)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


@router.get("/", response_model=list[schemas.Ingredient])
def list_ingredients(db: Session = Depends(get_db)):
    return db.query(models.Ingredient).all()


@router.delete("/{ingredients_id}")
def delete_chef(ingredients_id: int, db: Session = Depends(get_db)):
    ingredient = (
        db.query(models.Ingredient)
        .filter(models.Ingredient.id == ingredients_id)
        .first()
    )
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient is not found")

    db.delete(ingredient)
    db.commit()
    return {"message": "Ingredient is deleted"}


@router.put("/{ingredient_id}", response_model=schemas.Ingredient)
def update_ingredient(
    ingredient_id: int, data: schemas.IngredientUpdate, db: Session = Depends(get_db)
):
    ingredient = (
        db.query(models.Ingredient)
        .filter(models.Ingredient.id == ingredient_id)
        .first()
    )
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient is not found")

    for field, value in data.dict().items():
        if value is not None:
            setattr(ingredient, field, value)

    db.commit()
    db.refresh(ingredient)
    return ingredient
