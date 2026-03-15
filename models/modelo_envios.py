from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class logistica_terrestre(BaseModel):
    placa_vehiculo: str
    bodega_id: str
    
class logistica_maritima(BaseModel):
    numero_flota: str
    puerto_id: str
    
class Envios(BaseModel):

    numero_guia: str
    cliente_id: str
    producto_id: str

    cantidad_producto: int
    precio_envio: float

    fecha_registro: datetime
    fecha_entrega: datetime

    tipo_envio: str

    logistica: dict