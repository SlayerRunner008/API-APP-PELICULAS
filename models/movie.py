from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from config.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    genre = Column(String, nullable=False) 
    rating = Column(Float, default=0.0)
    image_url = Column(String)
    synopsis = Column(Text)
    director = Column(String, nullable=False)
    cast = Column(Text)

    favorites = relationship("Favorite", back_populates="movie", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")