from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from common_models.logger import logger, request_log
from functions_routers import main_router

app = FastAPI(title="Functions Servise")

origins = ["*"]
app.add_middleware(BaseHTTPMiddleware, dispatch=request_log)


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content={"detail": "This route is disabled"}, status_code=status.HTTP_403_FORBIDDEN)

app.include_router(main_router)

logger.info("API is started up")
