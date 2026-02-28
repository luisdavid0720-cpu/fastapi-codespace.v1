from pydantic import BaseModel
from Optional import Optional


class Usuario(BaseModel):
    id_usuario: int=None
    nombre: str
    cedula:str
    carrera:str
    semestre:int
    cargo: Optional[str] = None 
    celular:str
    correo:str
    id_rol:int
  
