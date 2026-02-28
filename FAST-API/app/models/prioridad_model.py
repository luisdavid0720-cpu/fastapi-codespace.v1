from pydantic import BaseModel

class Prioridad(BaseModel):
    id_prioridad: int = None
    nombre: str
 