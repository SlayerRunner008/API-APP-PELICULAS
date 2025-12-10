from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from config.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    year = Column(Integer, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    genres = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    synopsis = Column(Text, nullable=True)
    director = Column(String, nullable=True)
    cast = Column(Text, nullable=True)

    favorites = relationship("Favorite", back_populates="movie", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")