from pydantic import BaseModel

class tipo_incidencia(BaseModel):
    id_tipo : int=None
    nombre: str
    incidencias: str
