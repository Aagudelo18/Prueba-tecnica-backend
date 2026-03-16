from fastapi import APIRouter, Depends
from models.modelo_puertos import Puertos
from bson import ObjectId
from db.config import db
from seguridad import validar_token

router = APIRouter(tags=["puertos"])

@router.get("/puertos")
def lista_puerto(user=Depends(validar_token)):
    puertos = list(db.puertos.find())
    
    for puerto in puertos:
        puerto ["_id"] = str(puerto["_id"])
        
    return puertos

@router.get("/puertos/{puerto_id}")
def capturar_puerto(puerto_id:str,user=Depends(validar_token)):
    
    puerto = db.puertos.find_one({"_id":ObjectId(puerto_id)})
    
    if puerto:
        puerto["_id"] = str(puerto["_id"])
        return puerto
    
    return {"Error": "Puerto no encontrado"}

@router.post("/puertos")
async def crear_puertos(puerto:Puertos, user=Depends(validar_token)):
     nuevo_puerto = puerto.dict()
     resultado= db.puertos.insert_one(nuevo_puerto)

     return {"mensaje": "El puerto fue creado correctamente", "id_puerto": str(resultado.inserted_id)}
 
@router.put("/puertos/{puertos_id}")
def actualizar_puerto(puerto_id: str, puerto:Puertos, user=Depends(validar_token)):
    
    datos_actualizar = puerto.dict()
    
    resultado = db.puertos.update_one(
        {"_id": ObjectId(puerto_id)},
        {"$set": datos_actualizar}
    )
    
    if resultado.modified_count == 1:
        return {"Mensaje": "Puerto actualizado correctamente"}
    return{"mensaje": "No hubo ningun cambio"}

@router.delete("/puertos/{puerto_id}")
def eliminar_puertos(puerto_id:str,user=Depends(validar_token)):
    
    resultado = db.puertos.delete_one({"_id": ObjectId(puerto_id)})
    
    if resultado.deleted_count == 1:
        return {"Mensaje": "Puerto eliminado correctamente"}
    return {"Error": "Puerto no encontrado"}
