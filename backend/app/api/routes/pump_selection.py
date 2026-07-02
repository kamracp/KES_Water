from fastapi import APIRouter

from app.engineering_core.pumps.calculator import (
    PumpSelectionInput,
    PumpSelectionResult,
    calculate_pump_selection,
)

router = APIRouter(
    prefix="/pump-selection",
    tags=["Pump Selection"],
)


@router.post(
    "/calculate",
    response_model=PumpSelectionResult,
)
def calculate(data: PumpSelectionInput):
    return calculate_pump_selection(data)