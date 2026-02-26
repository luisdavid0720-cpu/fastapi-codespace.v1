from fastapi import APIRouter, HTTPException
from controllers.priodridad_controller import *
from models.prioridad_model import prioridad

router = APIRouter()

nuevo_prioridad = prioridadController()


@router.post("/create_prioridad")
async def create_prioridad(prioridad: prioridad):
    rpta = nuevo_prioridad.create_prioridad(prioridad)
    return rpta


@router.get("/get_prioridad/{prioridad_id}",response_model=prioridad)
async def get_prioridad(prioridad_id: int):
    rpta = nuevo_prioridad.get_prioridad(prioridad_id)
    return rpta

@router.get("/get_prioridades/")
async def get_prioridades():
    rpta = nuevo_prioridad.get_prioridades()
    return rpta