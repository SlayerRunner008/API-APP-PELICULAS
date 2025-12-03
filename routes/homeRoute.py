from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Home"])
def message():
    return {"message": "Bienvenido a la API de la app de películas"}