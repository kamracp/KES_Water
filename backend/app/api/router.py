from fastapi import APIRouter

from app.api.engineering_water_balance import (
    router as engineering_water_balance_router,
)
from app.api.health import router as health_router
from app.api.organization import router as organization_router
from app.api.plant import router as plant_router
from app.api.water_accounting_zone import (
    router as water_accounting_zone_router,
)


api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(organization_router)
api_router.include_router(plant_router)
api_router.include_router(water_accounting_zone_router)
api_router.include_router(engineering_water_balance_router)