import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer

from common_models.config import settings

security = HTTPBearer()

async def get_credentials(token: str = Security(security)) -> dict:
    """Зависимость для извлечения и проверки токена"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise credentials_exception
