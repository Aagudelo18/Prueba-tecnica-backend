from fastapi import APIRouter
from models.modelo_productos import Productos
from bson import ObjectId
from db.config import db


router = APIRouter(tags=["productos"])

@router.get("/productos")
def lista_producto():
    productos = list(db.productos.find())
    
    for producto in productos:
        producto ["_id"] = str(producto["_id"])
        
    return productos

@router.get("/productos/{producto_id}")
def capturar_producto(producto_id:str):
    
    producto = db.productos.find_one({"_id":ObjectId(producto_id)})
    
    if producto:
        producto["_id"] = str(producto["_id"])
        return producto
    
    return {"Error": "Producto no encontrado"}

@router.post("/productos")
async def crear_productos(producto:Productos):
     nuevo_producto = producto.dict()
     resultado= db.productos.insert_one(nuevo_producto)

     return {"mensaje": "Producto creado correctamente", "id_producto": str(resultado.inserted_id)}
 
@router.put("/productos/{producto_id}")
def actualizar_producto(producto_id: str, producto:Productos):
    
    datos_actualizar = producto.dict()
    
    resultado = db.productos.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": datos_actualizar}
    )
    
    if resultado.modified_count == 1:
        return {"Mensaje": "Producto actualizado correctamente"}
    return{"mensaje": "No hubo ningun cambio"}

@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id:str):
    
    resultado = db.productos.delete_one({"_id": ObjectId(producto_id)})
    
    if resultado.deleted_count == 1:
        return {"Mensaje": "Producto eliminado correctamente"}
    return {"Error": "producto no encontrado"}