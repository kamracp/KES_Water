from fastapi import APIRouter

from app.engineering_core.pumps.head_calculator import (
    PumpHeadInput,
    PumpHeadResult,
    calculate_pump_head,
)

router = APIRouter(
    prefix="/pump-head",
    tags=["Pump Head"],
)


@router.post(
    "/calculate",
    response_model=PumpHeadResult,
)
def calculate(data: PumpHeadInput):
    return calculate_pump_head(data)