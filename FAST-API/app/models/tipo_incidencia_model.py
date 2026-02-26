from pydantic import BaseModel

class Tipo_incidencia(BaseModel):
    id_tipo : int=None
    nombre: str
    incidencias: str
