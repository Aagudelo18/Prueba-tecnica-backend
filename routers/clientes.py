from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/clientes", 
                   tags=["clientes"],
                   responses={404:{"description": "No encontrado"}})


 