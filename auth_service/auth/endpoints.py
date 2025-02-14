from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.authentication_utils import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    oauth2_scheme,
)
from auth.crud import auth_crud
from auth.exceptions import (
    incorrect_data_exception,
    credentials_exception,
    expired_token_exception,
)
from common_models.config import settings
from common_models.db import get_async_session

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    db_credentials = await authenticate_user(
        username=form_data.username, password=form_data.password, session=session
    )
    if not db_credentials:
        raise incorrect_data_exception
    access_token_expires = timedelta(minutes=settings.token_expired_minutes)
    access_token = create_access_token(
        data={
            "sub": db_credentials.username,
            "user_id": db_credentials.id,
        },
        expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=settings.refresh_token_expire_minutes)
    refresh_token = create_refresh_token(data={"sub": db_credentials.username}, expires_delta=refresh_token_expires)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh_access_token(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = jwt.decode(
            token, settings.refresh_secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise expired_token_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    db_credentials = await auth_crud.get_db_credentials_by_username(username=username, session=session)
    if db_credentials is None:
        raise credentials_exception

    access_token_expires = timedelta(minutes=settings.token_expired_minutes)
    access_token = create_access_token(
        data={
            "sub": db_credentials.username,
            "user_id": db_credentials.id,
        },
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
