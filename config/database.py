import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Render te da la variable DATABASE_URL en el dashboard de la base
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()