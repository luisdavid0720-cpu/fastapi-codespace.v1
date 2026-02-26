from pydantic import BaseModel

class Historial_estado(BaseModel):
    id_historial: int = None
    fecha: str
    id_incidencia:str
    id_estado:str
    estado:str
