from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"

security = HTTPBearer()


def validar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload

    except JWTError:

        raise HTTPException(
            status_code=403,
            detail="Token inválido"
        )