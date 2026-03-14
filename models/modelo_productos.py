from pydantic import BaseModel

class Productos(BaseModel):
    nombre : str
    descripcion : str