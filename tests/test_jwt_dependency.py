from unittest.mock import patch

import jwt
import pytest
from fastapi import HTTPException, status

from common_models.config import settings
from common_models.jwt_dependency import get_credentials


@pytest.fixture
def mock_jwt_decode():
    with patch("common_models.jwt_dependency.jwt.decode") as mock_decode:
        yield mock_decode


@pytest.mark.asyncio
async def test_get_credentials_valid_token(mock_jwt_decode):
    """Тест на валидный токен"""
    valid_token = "valid_token"
    mock_payload = {"sub": "user_id", "exp": 1234567890}
    mock_jwt_decode.return_value = mock_payload

    token = type("Token", (), {"credentials": valid_token})
    result = await get_credentials(token=token)

    mock_jwt_decode.assert_called_once_with(valid_token, settings.secret_key, algorithms=[settings.algorithm])
    assert result == mock_payload


@pytest.mark.asyncio
async def test_get_credentials_expired_token(mock_jwt_decode):
    """Тест на истекший токен"""
    expired_token = "expired_token"
    mock_jwt_decode.side_effect = jwt.ExpiredSignatureError("Token has expired")

    token = type("Token", (), {"credentials": expired_token})

    with pytest.raises(HTTPException) as exc_info:
        await get_credentials(token=token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Token has expired"


@pytest.mark.asyncio
async def test_get_credentials_invalid_token(mock_jwt_decode):
    """Тест на недействительный токен"""
    invalid_token = "invalid_token"
    mock_jwt_decode.side_effect = jwt.InvalidTokenError("Invalid token")

    token = type("Token", (), {"credentials": invalid_token})

    with pytest.raises(HTTPException) as exc_info:
        await get_credentials(token=token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"
