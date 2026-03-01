from pydantic import BaseModel
from datetime import datetime

class Respuesta(BaseModel):
    id_respuesta: int=None
    mensaje: str
    fecha: datetime
    id_pqr: int
    id_usuario:int
