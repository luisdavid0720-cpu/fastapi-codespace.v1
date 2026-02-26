from pydantic import BaseModel
from typing import Optional
from datetime import date

class Historial_estado(BaseModel):
    id_historial: Optional[int] = None
    fecha: date
    id_incidencia: int
    id_estado: int
    estado: str