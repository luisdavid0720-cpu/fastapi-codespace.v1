from fastapi import APIRouter, HTTPException
from controllers.rol_controller import *
from models.rol_model import rol

router = APIRouter()

nuevo_rol = rol_controller()


@router.post("/create_rol")
async def create_rol(rol: rol):
    rpta = nuevo_rol.create_rol(rol)
    return rpta


@router.get("/get_rol/{rol_id}",response_model=rol)
async def get_rol(rol_id: int):
    rpta = nuevo_rol.get_rol(rol_id)
    return rpta

@router.get("/get_roles/")
async def get_roles():
    rpta = nuevo_rol.get_roles()
    return rpta