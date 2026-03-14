from fastapi import FastAPI
from routers import clientes,productos


app = FastAPI()

app.include_router(clientes.router)
app.include_router(productos.router)

@app.get("/")
async def root():
    return "Hola FastAPI!"



