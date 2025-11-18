from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

@router.post("/", response_model=schemas.Ingredient)
def create_ingredient(data: schemas.IngredientCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Ingredient).filter(models.Ingredient.name == data.name).first()
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
