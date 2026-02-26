from pydantic import BaseModel
from datetime import date
from typing import Optional

class Incidencia(BaseModel):
    id_incidencias: Optional[int] = None
    fecha: date
    descripcion: str
    id_usuario: str
    id_tipo: str
    id_estado: str
    id_departamento: str
    id_prioridad: str
    departamento: str
    estado: str
    prioridad: str
    tipo_incidencia: str