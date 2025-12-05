from fastapi import FastAPI
from routes import homeRoute,userRoute,movieRoute,favoritesRoutes,reviewRoutes
from config.database import engine, Base

app = FastAPI()
app.title = "Movies_APP_API"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

app.include_router(homeRoute.router)
app.include_router(userRoute.router)
app.include_router(movieRoute.router)
app.include_router(favoritesRoutes.router)
app.include_router(reviewRoutes.router)

