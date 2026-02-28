from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_usuario: Optional[int] =None
    nombre: str
    cedula:str
    carrera:str
    semestre:int
    cargo: Optional [str] = None
    celular:str
    correo:str
    id_rol:int
  
