from pydantic import BaseModel
from datetime import date


class Pqr(BaseModel):
    id_pqr: int = None
    descripcion: str
    fecha: date
    id_usuario:int
    id_tipo: int
    id_estado: int
    id_departamento: int
    id_prioridad: int
   