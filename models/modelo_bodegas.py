from pydantic import BaseModel

class Bodegas(BaseModel):
    nombre : str
    ciudad : str
    pais: str
    