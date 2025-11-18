from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.post("/", response_model=schemas.Restaurant)
def create_restaurant(data: schemas.RestaurantBase, db: Session = Depends(get_db)):
    rest = models.Restaurant(**data.dict())
    db.add(rest)
    db.commit()
    db.refresh(rest)
    return rest


@router.get("/", response_model=list[schemas.Restaurant])
def list_restaurants(db: Session = Depends(get_db)):
    return db.query(models.Restaurant).all()


@router.get("/{restaurant_id}/menu/", response_model=schemas.RestaurantMenuResponse)
def restaurant_menu(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant is not found")

    menu = [
        schemas.PizzaInMenu(
            name=p.name,
            cheese_type=p.cheese_type,
            dough_type=p.dough_type,
            secret_ingredient=p.secret_ingredient,
            ingredients=[i.name for i in p.ingredients],
        )
        for p in restaurant.pizzas
    ]

    return schemas.RestaurantMenuResponse(restaurant=restaurant.name, menu=menu)


@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant is not found")
    db.delete(restaurant)
    db.commit()
    return {"message": "Restaurant is deleted"}


@router.put("/{restaurant_id}", response_model=schemas.Restaurant)
def update_restaurant(
    restaurant_id: int, data: schemas.RestaurantUpdate, db: Session = Depends(get_db)
):
    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant is not found")

    for field, value in data.dict().items():
        if value is not None:
            setattr(restaurant, field, value)

    db.commit()
    db.refresh(restaurant)
    return restaurant
