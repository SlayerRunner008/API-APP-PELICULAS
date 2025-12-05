from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
from fastapi import APIRouter,  HTTPException
from config.database import Session as Session
from models.user import User

router = APIRouter(prefix="/users", tags=["users"])

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    db = Session()
    # Verificar si ya existe
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username ya registrado")

    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Guardar la contraseña
    new_user = User(username=user.username, email=user.email, password_hash=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user: UserLogin):
    db = Session()
    try:
        # Buscar usuario por email
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        # Comparar contraseña directamente (sin encriptar)
        if db_user.password_hash != user.password:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        return {
            "message": "Login exitoso",
            "user_id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        }
    finally:
        db.close()


@router.get("/", response_model=list[UserResponse])
def get_users():
    db = Session()
    try:
        users = db.query(User).all()
        return users
    finally:
        db.close()



@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    db = Session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    finally:
        db.close()


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    db = Session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if user_update.username is not None:
            user.username = user_update.username
        if user_update.email is not None:
            user.email = user_update.email
        if user_update.password is not None:
            user.password_hash = user_update.password

        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


@router.delete("/{user_id}")
def delete_user(user_id: int):
    db = Session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db.delete(user)
        db.commit()
        return {"message": "Usuario eliminado"}
    finally:
        db.close()


