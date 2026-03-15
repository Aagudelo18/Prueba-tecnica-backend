from fastapi import APIRouter, HTTPException
from models.modelo_envios import Envios
from bson import ObjectId
from db.config import db
import re


router = APIRouter(tags=["envios"])

@router.post("/envios")
def crear_envio(envio: Envios):

    if envio.cantidad_producto <= 0:
        raise HTTPException(status_code=400, detail="Cantidad debe ser mayor a 0")

    guia = db.envios.find_one({"numero_guia": envio.numero_guia})

    if guia:
        raise HTTPException(status_code=400, detail="Numero de guia ya existe")

    cliente = db.clientes.find_one({"_id": ObjectId(envio.cliente_id)})

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no existe")

    logistica = envio.logistica

    if envio.tipo_envio == "terrestre":

        if "placa_vehiculo" not in logistica or "bodega_id" not in logistica:
            raise HTTPException(status_code=400, detail="Datos de logistica terrestre incompletos")

        placa = logistica["placa_vehiculo"]

        if not re.match(r'^[A-Z]{3}[0-9]{3}$', placa):
            raise HTTPException(status_code=400, detail="Formato placa invalido AAA123")

    if envio.tipo_envio == "maritimo":

        if "numero_flota" not in logistica or "puerto_id" not in logistica:
            raise HTTPException(status_code=400, detail="Datos de logistica maritima incompletos")

        flota = logistica["numero_flota"]

        if not re.match(r'^[A-Z]{3}[0-9]{4}[A-Z]$', flota):
            raise HTTPException(status_code=400, detail="Formato flota invalido AAA1234A")

    precio_final = envio.precio_envio

    if envio.cantidad_producto > 10:

        if envio.tipo_envio == "terrestre":
            precio_final = envio.precio_envio * 0.95

        if envio.tipo_envio == "maritimo":
            precio_final = envio.precio_envio * 0.97

    data = envio.dict()
    
    data["cliente_id"] = ObjectId(data["cliente_id"])
    data["producto_id"] = ObjectId(data["producto_id"])

    if envio.tipo_envio == "maritimo":
     data["logistica"]["puerto_id"] = ObjectId(data["logistica"]["puerto_id"])

    if envio.tipo_envio == "terrestre":
     data["logistica"]["bodega_id"] = ObjectId(data["logistica"]["bodega_id"])

    data["precio_envio"] = precio_final

    resultado = db.envios.insert_one(data)

    return {
        "mensaje": "Envio creado",
        "precio_final": precio_final,
        "id": str(resultado.inserted_id)
    }
