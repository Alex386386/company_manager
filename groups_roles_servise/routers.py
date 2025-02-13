from fastapi import APIRouter

from groups.endpoints import router as groups_router
from role_dicts.endpoints import router as role_dicts_router

main_router = APIRouter(prefix="/api")
main_router.include_router(groups_router)
main_router.include_router(role_dicts_router)