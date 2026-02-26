from pydantic import BaseModel
from datetime import date


class Pqr(BaseModel):
    id_pqrs: int = None
    descripcion: str
    fecha: date
    id_usuario:int
    id_tipo: int
    id_estado: int
    id_departamento: int
    id_prioridad: int
    evidencias: str
    historial_estado: str
    departamento: str
    estado: str
    prioridad:str
    tipo_pqr:str
    usuario:str
    respuesta:str