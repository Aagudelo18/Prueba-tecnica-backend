from fastapi import APIRouter, HTTPException, Depends
from db.config import db
from models.modelo_usuarios import Usuario
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"


def crear_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=2)

    data.update({"exp": expire})

    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return token

@router.post("/registro")
def registrar(usuario: Usuario):

    usuario_existente = db.usuarios.find_one({"username": usuario.username})

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    password_hash = pwd_context.hash(usuario.password)

    db.usuarios.insert_one({
        "username": usuario.username,
        "password": password_hash
    })

    return {"mensaje": "Usuario creado"}

@router.post("/login")
def login(usuario: Usuario):

    user = db.usuarios.find_one({"username": usuario.username})

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if not pwd_context.verify(usuario.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token({
        "sub": user["username"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }