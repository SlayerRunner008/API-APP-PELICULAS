from fastapi import FastAPI
from routes import homeRoute

app = FastAPI()
app.title = "Movies_APP_API"
app.version = "0.0.1"

app.include_router(homeRoute.router)
