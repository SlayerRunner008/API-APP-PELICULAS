from fastapi import APIRouter, HTTPException
from config.database import Session
from models.movie import Movie
from pydantic import BaseModel

router = APIRouter(prefix="/movies", tags=["movies"])

# ---------------------------
# Schemas Pydantic
# ---------------------------
class MovieCreate(BaseModel):
    title: str
    year: int
    duration_minutes: int
    genre: str
    rating: float | None = None
    image_url: str | None = None
    synopsis: str | None = None
    director: str
    cast: str | None = None

class MovieUpdate(BaseModel):
    title: str | None = None
    year: int | None = None
    duration_minutes: int | None = None
    genre: str | None = None
    rating: float | None = None
    image_url: str | None = None
    synopsis: str | None = None
    director: str | None = None
    cast: str | None = None

class MovieResponse(BaseModel):
    id: int
    title: str
    year: int
    duration_minutes: int
    genre: str
    rating: float | None
    image_url: str | None
    synopsis: str | None
    director: str
    cast: str | None

    class Config:
        orm_mode = True

# ---------------------------
# CRUD Endpoints
# ---------------------------
@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate):
    db = Session()
    try:
        new_movie = Movie(**movie.dict())
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)
        return new_movie
    finally:
        db.close()

@router.get("/", response_model=list[MovieResponse])
def get_movies():
    db = Session()
    try:
        movies = db.query(Movie).all()
        return movies
    finally:
        db.close()

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int):
    db = Session()
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        return movie
    finally:
        db.close()

@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie_update: MovieUpdate):
    db = Session()
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Película no encontrada")

        for field, value in movie_update.dict(exclude_unset=True).items():
            setattr(movie, field, value)

        db.commit()
        db.refresh(movie)
        return movie
    finally:
        db.close()

@router.delete("/{movie_id}")
def delete_movie(movie_id: int):
    db = Session()
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Película no encontrada")

        db.delete(movie)
        db.commit()
        return {"message": "Película eliminada"}
    finally:
        db.close()