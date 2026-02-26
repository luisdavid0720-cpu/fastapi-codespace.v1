from pydantic import BaseModel

class Usuario(BaseModel):
    id_usuario: int=None
    nombre: str
    cedula:str
    carrera:str
    semestre:str
    cargo:str
    celular:str
    correo:str
    id_rol:str
    rol:str
