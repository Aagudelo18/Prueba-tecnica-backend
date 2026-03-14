from fastapi import FastAPI
from routers import clientes,productos, bodegas, puertos


app = FastAPI()

app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(bodegas.router)
app.include_router(puertos.router)

@app.get("/")
async def root():
    return "Hola FastAPI!"



