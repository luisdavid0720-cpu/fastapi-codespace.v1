from pydantic import BaseModel


class Departamento(BaseModel):
    id_departamento: int = None
    nombre: str
   