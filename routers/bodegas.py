from fastapi import APIRouter, Depends
from models.modelo_bodegas import Bodegas
from bson import ObjectId
from db.config import db
from seguridad import validar_token


router = APIRouter(tags=["bodegas"])

@router.get("/bodegas")
def lista_bodega(user=Depends(validar_token)):
    bodegas = list(db.bodegas.find())
    
    for bodega in bodegas:
        bodega ["_id"] = str(bodega["_id"])
        
    return bodegas

@router.get("/bodegas/{bodega_id}")
def capturar_bodega(bodega_id:str, user=Depends(validar_token)):
    
    bodega = db.bodegas.find_one({"_id":ObjectId(bodega_id)})
    
    if bodega:
        bodega["_id"] = str(bodega["_id"])
        return bodega
    
    return {"Error": "Bodega no encontrado"}

@router.post("/bodegas")
async def crear_bodegas(bodega:Bodegas, user=Depends(validar_token)):
     nueva_bodega = bodega.dict()
     resultado= db.bodegas.insert_one(nueva_bodega)

     return {"mensaje": "Bodega creada correctamente", "id_bodega": str(resultado.inserted_id)}
 
@router.put("/bodegas/{bodega_id}")
def actualizar_bodega(bodega_id: str, bodega:Bodegas, user=Depends(validar_token)):
    
    datos_actualizar = bodega.dict()
    
    resultado = db.bodegas.update_one(
        {"_id": ObjectId(bodega_id)},
        {"$set": datos_actualizar}
    )
    
    if resultado.modified_count == 1:
        return {"Mensaje": "La bodega se actualizo correctamente"}
    return{"mensaje": "No hubo ningun cambio"}

@router.delete("/bodegas/{bodega_id}")
def eliminar_bodega(bodega_id:str,user=Depends(validar_token)):
    
    resultado = db.bodegas.delete_one({"_id": ObjectId(bodega_id)})
    
    if resultado.deleted_count == 1:
        return {"Mensaje": "Bodega eliminada correctamente"}
    return {"Error": "Bodega no encontrada"}