from pydantic import BaseModel

class Clientes(BaseModel):
    nombre: str
    celular: str
    correo: str
    direccion: str