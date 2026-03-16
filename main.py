from fastapi import FastAPI
from routers import clientes,productos, bodegas, puertos,envios
from fastapi.middleware.cors import CORSMiddleware
from routers import autenticacion

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(bodegas.router)
app.include_router(puertos.router)
app.include_router(envios.router)
app.include_router(autenticacion.router)

@app.get("/")
async def gestion_logistica():
    return "Bienvenidos a la API de alejandra agudelo de gestion de logistica de envios"



