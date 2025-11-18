from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/chefs", tags=["Chefs"])


@router.post("/", response_model=schemas.Chef)
def create_chef(data: schemas.ChefCreate, db: Session = Depends(get_db)):
    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == data.restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    chef = models.Chef(**data.dict())
    db.add(chef)
    db.commit()
    db.refresh(chef)
    return chef


@router.get("/", response_model=list[schemas.Chef])
def list_chefs(db: Session = Depends(get_db)):
    return db.query(models.Chef).all()
