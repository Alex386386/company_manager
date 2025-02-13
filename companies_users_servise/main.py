from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from common_models.logger import logger, request_log
from initial_data import load_initial_data
from routers import main_router


@asynccontextmanager
async def load_data_lifespan(app: FastAPI):
    logger.debug("Подготовка начальных данных.")
    await load_initial_data()
    logger.debug("Приложение запущено.")
    yield


app = FastAPI(title="Companies Users Servise", lifespan=load_data_lifespan)

origins = ["*"]
app.add_middleware(BaseHTTPMiddleware, dispatch=request_log)


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content={"detail": "This route is disabled"}, status_code=status.HTTP_403_FORBIDDEN)

app.include_router(main_router)

logger.info("API is started up")
