from fastapi import APIRouter

from functions.endpoints import router as functions_router

main_router = APIRouter(prefix="/api")
main_router.include_router(functions_router)
