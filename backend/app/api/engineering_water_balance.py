from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.water_balance import (
    WaterBalanceCalculationRequest,
    WaterBalanceCalculationResponse,
)
from app.services.water_balance_service import (
    WaterBalanceCalculationService,
)


router = APIRouter(
    prefix="/engineering/water-balance",
    tags=["Engineering - Water Balance"],
)


@router.post(
    "/calculate",
    response_model=WaterBalanceCalculationResponse,
    summary="Calculate enterprise water balance",
    description=(
        "Calculate a boundary-aware water balance using the audit "
        "tolerance configured for the selected Water Accounting Zone."
    ),
)
def calculate_enterprise_water_balance(
    payload: WaterBalanceCalculationRequest,
    db: Session = Depends(get_db),
) -> WaterBalanceCalculationResponse:
    service = WaterBalanceCalculationService(db)
    return service.calculate(payload)