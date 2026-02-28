from pydantic import BaseModel

class Evidencia(BaseModel):
    id_evidencia: int = None
    nombre_archivo: str
    url:str
    id_pqr:int
