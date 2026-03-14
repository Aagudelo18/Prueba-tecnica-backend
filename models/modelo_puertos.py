from pydantic import BaseModel

class Puertos(BaseModel):
    nombre : str
    ciudad : str
    pais : str