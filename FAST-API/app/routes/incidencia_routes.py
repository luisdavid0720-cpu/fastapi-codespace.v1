from fastapi import APIRouter, HTTPException
from controllers.incidencia_controller import *
from models.incidencia_model import incidencia

router = APIRouter()

nuevo_incidencia = incidenciaController()


@router.post("/create_incidencia")
async def create_incidencia(incidencia: incidencia):
    rpta = nuevo_incidencia.create_incidencia(incidencia)
    return rpta


@router.get("/get_incidencia/{incidencia_id}",response_model=incidencia)
async def get_incidencia(incidencia_id: int):
    rpta = nuevo_usuario.get_incidencia(incidencia_id)
    return rpta

@router.get("/get_incidencias/")
async def get_incidencias():
    rpta = nuevo_incidencia.get_incidencias()
    return rpta