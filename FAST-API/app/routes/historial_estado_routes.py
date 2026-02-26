from fastapi import APIRouter, HTTPException
from controllers.historial_estado_controller import *
from models.historial_estado_model import historial_estado

router = APIRouter()

nuevo_historial_estado = historial_estado_Controller()


@router.post("/create_historial_estado")
async def create_historial_estado(historial_estado: historial_estado):
    rpta = nuevo_historial_estado.create_historial_estado(historial_estado)
    return rpta


@router.get("/get_historial_estado/{historial_estado_id}",response_model=historial_estado)
async def get_historial_estado(historial_estado_id: int):
    rpta = nuevo_historial_estado.get_historial_estado(historial_estado_id)
    return rpta

@router.get("/get_historial_estados/")
async def get_historial_estados():
    rpta = nuevo_historial_estado.get_historial_estados()
    return rpta