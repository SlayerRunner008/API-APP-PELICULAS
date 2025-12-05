from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from config.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    release_year = Column(Integer)
    genre = Column(String)
    poster_url = Column(String)
    rating = Column(Float, nullable=True) 

    favorites = relationship("Favorite", back_populates="movie", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")