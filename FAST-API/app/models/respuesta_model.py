from pydantic import BaseModel

class Respuesta(BaseModel):
    id_respuesta: int=None
    mensaje: str
    fecha:str
    id_incidencias: str
    id_usuario:str
