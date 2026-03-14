from fastapi import APIRouter, HTTPException, status
from models.modelo_clientes import Clientes
from bson import ObjectId
from db.config import db


router = APIRouter(tags=["clientes"])

@router.get("/clientes")
def lista_cliente():
    clientes = list(db.clientes.find())
    
    for cliente in clientes:
        cliente ["_id"] = str(cliente["_id"])
        
    return clientes

@router.get("/clientes/{cliente_id}")
def capturar_cliente(cliente_id:str):
    
    cliente = db.clientes.find_one({"_id":ObjectId(cliente_id)})
    
    if cliente:
        cliente["_id"] = str(cliente["_id"])
        return cliente
    
    return {"Error": "Cliente no encontrado"}

@router.post("/clientes")
async def crear_clientes(cliente:Clientes):
     nuevo_cliente = cliente.dict()
     resultado= db.clientes.insert_one(nuevo_cliente)

     return {"mensaje": "Cliente creado correctamente", "id_cliente": str(resultado.inserted_id)}
 
@router.put("/clientes/{cliente_id}")
def actualizar_cliente(cliente_id: str, cliente:Clientes):
    
    datos_actualizar = cliente.dict()
    
    resultado = db.clientes.update_one(
        {"_id": ObjectId(cliente_id)},
        {"$set": datos_actualizar}
    )
    
    if resultado.modified_count == 1:
        return {"Mensaje": "Cliente actualizado correctamente"}
    return{"mensaje": "No hubo ningun cambio"}

@router.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id:str):
    
    resultado = db.clientes.delete_one({"_id": ObjectId(cliente_id)})
    
    if resultado.deleted_count == 1:
        return {"Mensaje": "Cliente eliminado correctamente"}
    return {"Error": "cliente no encontrado"}
