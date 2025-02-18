from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from common_models.logger import logger
from common_models.utils import log_and_raise_error, check_exists_and_get_or_return_error


def test_log_and_raise_error():
    """Тест на логирование ошибки и вызов HTTPException."""
    message_log = "Test log message"
    message_error = "Test error message"
    status_code = HTTPStatus.BAD_REQUEST

    with patch.object(logger, "error") as mock_logger_error:
        with pytest.raises(HTTPException) as exc_info:
            log_and_raise_error(message_log, message_error, status_code)

        mock_logger_error.assert_called_once_with(message_log)

    assert exc_info.value.status_code == status_code
    assert exc_info.value.detail == message_error

@pytest.mark.asyncio
async def test_check_exists_and_get_or_return_error_success():
    """Тест на успешное получение объекта из базы данных."""
    db_id = 1
    mock_crud = MagicMock()
    mock_method = AsyncMock(return_value="mock_object")
    mock_crud.get_by_id = mock_method
    mock_session = AsyncMock()

    with patch.object(logger, "info") as mock_logger_info:
        result = await check_exists_and_get_or_return_error(
            db_id, mock_crud, "get_by_id", "Object not found", HTTPStatus.NOT_FOUND, mock_session
        )

        mock_method.assert_called_once_with(db_id, mock_session)

        assert result == "mock_object"

        mock_logger_info.assert_called_once_with(f"Объект с id или name ({db_id}) успешно получен из БД")

@pytest.mark.asyncio
async def test_check_exists_and_get_or_return_error_method_not_found():
    """Тест на вызов ошибки, если метод не найден в CRUD."""
    db_id = 1
    mock_crud = MagicMock()
    mock_crud.get_by_id = None
    mock_session = AsyncMock()

    with patch.object(logger, "error") as mock_logger_error:
        with pytest.raises(HTTPException) as exc_info:
            await check_exists_and_get_or_return_error(
                db_id, mock_crud, "get_by_id", "Object not found", HTTPStatus.NOT_FOUND, mock_session
            )

        assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert exc_info.value.detail == "Invalid method"
        mock_logger_error.assert_called_once_with("Метод get_by_id не найден в CRUD")

@pytest.mark.asyncio
async def test_check_exists_and_get_or_return_error_object_not_found():
    """Тест на вызов ошибки, если объект не найден в базе данных."""
    db_id = 1
    mock_crud = MagicMock()
    mock_method = AsyncMock(return_value=None)
    mock_crud.get_by_id = mock_method
    mock_session = AsyncMock()

    with patch.object(logger, "error") as mock_logger_error:
        with pytest.raises(HTTPException) as exc_info:
            await check_exists_and_get_or_return_error(
                db_id, mock_crud, "get_by_id", "Object not found", HTTPStatus.NOT_FOUND, mock_session
            )

        assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
        assert exc_info.value.detail == "Object not found"
        mock_logger_error.assert_called_once_with(f"Объект с id или name ({db_id}) не найден в БД")