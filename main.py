from fastapi import FastAPI
from routers import clientes

app = FastAPI()

app.include_router(clientes.router)

@app.get("/")
async def root():
    return "Hola FastAPI!"



