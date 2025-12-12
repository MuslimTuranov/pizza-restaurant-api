import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from .. import models, schemas
from ..dependencies import get_cache

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.get("/", response_model=list[schemas.Restaurant])
def list_restaurants(
    db: Session = Depends(get_db),
    cache_client = Depends(get_cache)
):

    restaurants = db.query(models.Restaurant).all()
    return restaurants

@router.get("/{restaurant_id}/menu/", response_model=schemas.RestaurantMenuResponse)
def restaurant_menu(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
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

    return schemas.RestaurantMenuResponse(
        restaurant=restaurant.name,
        menu=menu
    )

@router.post("/", response_model=schemas.Restaurant)
def create_restaurant(
    data: schemas.RestaurantCreate,
    db: Session = Depends(get_db)
):
    try:
        restaurant = models.Restaurant(**data.dict())
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)
        return restaurant
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Restaurant with this name already exists"
        )

@router.put("/{restaurant_id}", response_model=schemas.Restaurant)
def update_restaurant(
    restaurant_id: int,
    data: schemas.RestaurantUpdate,
    db: Session = Depends(get_db)
):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant is not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(restaurant, field, value)

    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.get("/ranking-by-rating")
def get_restaurants_by_rating(
    min_rating: float = 0,
    db: Session = Depends(get_db)
):
    restaurants_with_rating = (
        db.query(
            models.Restaurant,
            func.coalesce(func.avg(models.Review.rating), 0).label("avg_rating"),
        )
        .outerjoin(models.Review)
        .group_by(models.Restaurant.id)
        .having(func.coalesce(func.avg(models.Review.rating), 0) >= min_rating)
        .order_by(func.avg(models.Review.rating).desc())
        .all()
    )

    result = [
        {
            "id": r.Restaurant.id,
            "name": r.Restaurant.name,
            "address": r.Restaurant.address,
            "avg_rating": float(r.avg_rating),
        }
        for r in restaurants_with_rating
    ]

    return result

@router.get("/health/check-redis")
def check_redis(cache_client = Depends(get_cache)):
    try:
        cache_client.client.ping()
        return {"redis": "connected"}
    except Exception as e:
        return {"redis": "disconnected", "error": str(e)}