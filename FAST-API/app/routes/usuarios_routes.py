from fastapi import APIRouter, HTTPException
from controllers.usuarios_controller import *
from models.usuarios_model import Usuarios

router = APIRouter()

nuevo_usuario = UsuariosController()


@router.post("/create_usuarios")
async def create_usuarios(usuarios: Usuarios):
    rpta = nuevo_usuario.create_usuaios(usuarios)
    return rpta


@router.get("/get_usuarios/{usuarios_id}",response_model=Usuarios)
async def get_usuarios(usuarios_id: int):
    rpta = nuevo_usuario.get_usuarios(usuarios_id)
    return rpta

@router.get("/get_usuarios/")
async def get_usuarios():
    rpta = nuevo_usuario.get_usuarios()
    return rpta