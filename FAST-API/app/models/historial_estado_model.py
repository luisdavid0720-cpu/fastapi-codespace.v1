from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Historial_estado(BaseModel):
    id_historial: Optional[int] = None
    fecha: Optional[datetime] = None
    id_pqr: int
    id_estado: int