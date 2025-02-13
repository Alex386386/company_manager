from fastapi import APIRouter

from companies.endpoints import router as companies_router
from property_code_dicts.endpoints import router as property_code_dicts_router
from timezone_dict.endpoints import router as timezone_dict_router
from users.endpoints import router as users_router

main_router = APIRouter(prefix="/api")
main_router.include_router(property_code_dicts_router)
main_router.include_router(companies_router)
main_router.include_router(timezone_dict_router)
main_router.include_router(users_router)
