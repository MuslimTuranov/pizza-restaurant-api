from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=schemas.ReviewResponse)
def create_review(data: schemas.ReviewBase, db: Session = Depends(get_db)):
    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == data.restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    review = models.Review(**data.dict())
    db.add(review)
    db.commit()
    db.refresh(review)

    return schemas.ReviewResponse(
        id=review.id,
        rating=review.rating,
        text=review.text,
        restaurant_id=review.restaurant_id,
        restaurant_name=review.restaurant.name,
    )


@router.get("/", response_model=list[schemas.ReviewResponse])
def list_reviews(db: Session = Depends(get_db)):
    reviews = (
        db.query(models.Review).options(joinedload(models.Review.restaurant)).all()
    )
    return [
        schemas.ReviewResponse(
            id=r.id,
            rating=r.rating,
            text=r.text,
            restaurant_id=r.restaurant_id,
            restaurant_name=r.restaurant.name,
        )
        for r in reviews
    ]


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return {"message": "Review is deleted"}


@router.put("/{review_id}", response_model=schemas.ReviewResponse)
def update_review(
    review_id: int, data: schemas.ReviewUpdate, db: Session = Depends(get_db)
):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review is not found")

    for field, value in data.dict().items():
        if value is not None:
            setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review
