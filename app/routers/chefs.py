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


@router.delete("/{chef_id}")
def delete_chef(chef_id: int, db: Session = Depends(get_db)):
    chef = db.query(models.Chef).filter(models.Chef.id == chef_id).first()
    if not chef:
        raise HTTPException(status_code=404, detail="Chef is not found")

    db.delete(chef)
    db.commit()
    return {"message": "Chef is deleted"}


@router.put("/{chef_id}", response_model=schemas.Chef)
def update_chef(chef_id: int, data: schemas.ChefUpdate, db: Session = Depends(get_db)):
    chef = db.query(models.Chef).filter(models.Chef.id == chef_id).first()
    if not chef:
        raise HTTPException(status_code=404, detail="Chef is not found")

    for field, value in data.dict().items():
        if value is not None:
            setattr(chef, field, value)

    db.commit()
    db.refresh(chef)
    return chef
