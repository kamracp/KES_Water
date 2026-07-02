from fastapi import APIRouter

from app.engineering_core.water_balance.calculator import (
    WaterBalanceInput,
    WaterBalanceResult,
    calculate_water_balance,
)

router = APIRouter(prefix="/water-balance", tags=["Water Balance"])


@router.post("/calculate", response_model=WaterBalanceResult)
def calculate(data: WaterBalanceInput):
    return calculate_water_balance(data)
