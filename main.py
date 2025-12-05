from fastapi import FastAPI
from routes import homeRoute
from config.database import engine, Base

app = FastAPI()
app.title = "Movies_APP_API"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)


app.include_router(homeRoute.router)
