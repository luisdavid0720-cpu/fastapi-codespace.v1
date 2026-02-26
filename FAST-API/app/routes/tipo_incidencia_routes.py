from fastapi import APIRouter, HTTPException
from controllers.tipo_incidencia_controller import *
from models.tipo_incidencia_model import tipo_incidencia

router = APIRouter()

nuevo_tipo_incencia = tipo_incidencia_Controller()


@router.post("/create_tipo_incidencia")
async def create_tipo_incidencia(tipo_incidencia: tipo_incidencia):
    rpta = nuevo_tipo_incencia.create_tipo_incidencia(tipo_incidencia)
    return rpta


@router.get("/get_tipo_incidencia/{tipo_incidencia_id}",response_model=tipo_incidencia)
async def get_tipo_incidencia(tipo_incidencia_id: int):
    rpta = nuevo_tipo_incencia.get_tipo_incidencia(tipo_incidencia_id)
    return rpta

@router.get("/get_tipo_incidencias/")
async def get_tipo_incidencias():
    rpta = nuevo_tipo_incencia.get_tipo_incidencias()
    return rpta