from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from config.db_config import get_db_connection
from models.usuario import Usuario

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginRequest, db: Session):
    user = db.query(Usuario).filter(
        Usuario.email == data.email,
        Usuario.password == data.password
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {
        "mensaje": "Login correcto",
        "usuario": user.id_usuario
    }