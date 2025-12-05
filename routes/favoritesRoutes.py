from fastapi import APIRouter, HTTPException
from config.database import Session
from models.favorite import Favorite
from models.user import User
from models.movie import Movie
from pydantic import BaseModel

router = APIRouter(prefix="/favorites", tags=["favorites"])


class FavoriteCreate(BaseModel):
    user_id: int
    movie_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int

    class Config:
        orm_mode = True




@router.post("/", response_model=FavoriteResponse)
def add_favorite(favorite: FavoriteCreate):
    db = Session()
    try:

        user = db.query(User).filter(User.id == favorite.user_id).first()
        movie = db.query(Movie).filter(Movie.id == favorite.movie_id).first()
        if not user or not movie:
            raise HTTPException(status_code=404, detail="Usuario o película no encontrada")

        existing = db.query(Favorite).filter(
            Favorite.user_id == favorite.user_id,
            Favorite.movie_id == favorite.movie_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="La película ya está en favoritos")

        new_fav = Favorite(user_id=favorite.user_id, movie_id=favorite.movie_id)
        db.add(new_fav)
        db.commit()
        db.refresh(new_fav)
        return new_fav
    finally:
        db.close()

@router.get("/user/{user_id}", response_model=list[FavoriteResponse])
def get_user_favorites(user_id: int):
    db = Session()
    try:
        favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
        return favorites
    finally:
        db.close()

@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int):
    db = Session()
    try:
        fav = db.query(Favorite).filter(Favorite.id == favorite_id).first()
        if not fav:
            raise HTTPException(status_code=404, detail="Favorito no encontrado")

        db.delete(fav)
        db.commit()
        return {"message": "Favorito eliminado"}
    finally:
        db.close()