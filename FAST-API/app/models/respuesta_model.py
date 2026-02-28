from pydantic import BaseModel
from datetime import date

class Respuesta(BaseModel):
    id_respuesta: int=None
    mensaje: str
    fecha:date
    id_pqr: int
    id_usuario:int
