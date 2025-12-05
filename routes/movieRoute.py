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
    description: str | None = None
    release_year: int | None = None
    genre: str | None = None
    poster_url: str | None = None
    rating: float | None = None

class MovieUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    release_year: int | None = None
    genre: str | None = None
    poster_url: str | None = None
    rating: float | None = None

class MovieResponse(BaseModel):
    id: int
    title: str
    description: str | None
    release_year: int | None
    genre: str | None
    poster_url: str | None
    rating: float | None

    class Config:
        orm_mode = True


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