from fastapi import APIRouter

from settings.endpoints import router as settings_router
from settings_dict.endpoints import router as settings_dict_router

main_router = APIRouter(prefix="/api")
main_router.include_router(settings_dict_router)
main_router.include_router(settings_router)
