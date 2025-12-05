from fastapi import APIRouter, HTTPException
from config.database import Session
from models.review import Review
from models.user import User
from models.movie import Movie
from pydantic import BaseModel

router = APIRouter(prefix="/reviews", tags=["reviews"])

class ReviewCreate(BaseModel):
    content: str
    user_id: int
    movie_id: int

class ReviewUpdate(BaseModel):
    content: str | None = None

class ReviewResponse(BaseModel):
    id: int
    content: str
    user_id: int
    movie_id: int

    class Config:
        orm_mode = True



@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate):
    db = Session()
    try:
        user = db.query(User).filter(User.id == review.user_id).first()
        movie = db.query(Movie).filter(Movie.id == review.movie_id).first()
        if not user or not movie:
            raise HTTPException(status_code=404, detail="Usuario o película no encontrada")

        new_review = Review(content=review.content, user_id=review.user_id, movie_id=review.movie_id)
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
    finally:
        db.close()

@router.get("/", response_model=list[ReviewResponse])
def get_all_reviews():
    db = Session()
    try:
        reviews = db.query(Review).all()
        return reviews
    finally:
        db.close()

@router.get("/user/{user_id}", response_model=list[ReviewResponse])
def get_user_reviews(user_id: int):
    db = Session()
    try:
        reviews = db.query(Review).filter(Review.user_id == user_id).all()
        return reviews
    finally:
        db.close()

@router.get("/movie/{movie_id}", response_model=list[ReviewResponse])
def get_movie_reviews(movie_id: int):
    db = Session()
    try:
        reviews = db.query(Review).filter(Review.movie_id == movie_id).all()
        return reviews
    finally:
        db.close()

@router.put("/user/{user_id}/review/{review_id}", response_model=ReviewResponse)
def update_review(user_id: int, review_id: int, review_update: ReviewUpdate):
    db = Session()
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Reseña no encontrada")

        if review.user_id != user_id:
            raise HTTPException(status_code=403, detail="No puedes modificar reseñas de otros usuarios")

        if review_update.content is not None:
            review.content = review_update.content

        db.commit()
        db.refresh(review)
        return review
    finally:
        db.close()

@router.delete("/user/{user_id}/review/{review_id}")
def delete_review(user_id: int, review_id: int):
    db = Session()
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Reseña no encontrada")

        if review.user_id != user_id:
            raise HTTPException(status_code=403, detail="No puedes eliminar reseñas de otros usuarios")

        db.delete(review)
        db.commit()
        return {"message": "Reseña eliminada"}
    finally:
        db.close()