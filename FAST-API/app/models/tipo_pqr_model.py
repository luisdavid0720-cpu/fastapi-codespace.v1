from pydantic import BaseModel

class Tipo_pqr(BaseModel):
    id_tipo : int=None
    nombre: str
    pqrs: str
