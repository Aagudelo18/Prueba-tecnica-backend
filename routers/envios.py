from fastapi import APIRouter, Depends, HTTPException
from models.modelo_envios import Envios
from bson import ObjectId
from db.config import db
import re
from seguridad import validar_token

router = APIRouter(tags=["envios"])

@router.get("/envios")
def listar_envios(user=Depends(validar_token)):

    envios = list(db.envios.find())

    for envio in envios:
        envio["_id"] = str(envio["_id"])
        envio["cliente_id"] = str(envio["cliente_id"])
        envio["producto_id"] = str(envio["producto_id"])

        if envio["tipo_envio"] == "terrestre":
            envio["logistica"]["bodega_id"] = str(envio["logistica"]["bodega_id"])

        if envio["tipo_envio"] == "maritimo":
            envio["logistica"]["puerto_id"] = str(envio["logistica"]["puerto_id"])

    return envios

@router.get("/envios/{envio_id}")
def obtener_envio(envio_id: str, user=Depends(validar_token)):

    envio = db.envios.find_one({"_id": ObjectId(envio_id)})

    if not envio:
        raise HTTPException(status_code=404, detail="Envio no encontrado")

    envio["_id"] = str(envio["_id"])
    envio["cliente_id"] = str(envio["cliente_id"])
    envio["producto_id"] = str(envio["producto_id"])

    if envio["tipo_envio"] == "terrestre":
        envio["logistica"]["bodega_id"] = str(envio["logistica"]["bodega_id"])

    if envio["tipo_envio"] == "maritimo":
        envio["logistica"]["puerto_id"] = str(envio["logistica"]["puerto_id"])

    return envio

@router.post("/envios")
def crear_envio(envio: Envios, user=Depends(validar_token)):

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
            raise HTTPException(status_code=400, detail="Formato placa invalido debe contener tres letras iniciales y tres numero finales")

    if envio.tipo_envio == "maritimo":

        if "numero_flota" not in logistica or "puerto_id" not in logistica:
            raise HTTPException(status_code=400, detail="Datos de logistica maritima incompletos")

        flota = logistica["numero_flota"]

        if not re.match(r'^[A-Z]{3}[0-9]{4}[A-Z]$', flota):
            raise HTTPException(status_code=400, detail="Formato flota invalido, debe contener tres letras iniciales, tres numeros y una letra final")

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
    
@router.put("/envios/{envio_id}")
def actualizar_envio(envio_id: str, envio: Envios, user=Depends(validar_token)):

    if envio.cantidad_producto <= 0:
        raise HTTPException(status_code=400, detail="Cantidad debe ser mayor a 0")

    logistica = envio.logistica

    if envio.tipo_envio == "terrestre":

        if "placa_vehiculo" not in logistica or "bodega_id" not in logistica:
            raise HTTPException(status_code=400, detail="Datos de logistica terrestre incompletos")

        placa = logistica["placa_vehiculo"]

        if not re.match(r'^[A-Z]{3}[0-9]{3}$', placa):
            raise HTTPException(status_code=400, detail="Formato placa invalido")

    if envio.tipo_envio == "maritimo":

        if "numero_flota" not in logistica or "puerto_id" not in logistica:
            raise HTTPException(status_code=400, detail="Datos de logistica maritima incompletos")

        flota = logistica["numero_flota"]

        if not re.match(r'^[A-Z]{3}[0-9]{4}[A-Z]$', flota):
            raise HTTPException(status_code=400, detail="Formato flota invalido")

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

    resultado = db.envios.update_one(
        {"_id": ObjectId(envio_id)},
        {"$set": data}
    )

    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Envio no actualizado")

    return {
        "mensaje": "Envio actualizado",
        "precio_final": precio_final
    }
    
@router.delete("/envios/{envio_id}")
def eliminar_envio(envio_id: str, user=Depends(validar_token)):

    resultado = db.envios.delete_one({"_id": ObjectId(envio_id)})

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Envio no encontrado")

    return {"mensaje": "Envio eliminado correctamente"}

