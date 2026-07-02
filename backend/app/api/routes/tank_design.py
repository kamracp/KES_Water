from fastapi import APIRouter

from app.engineering_core.tanks.calculator import (
    TankInput,
    TankResult,
    calculate_tank,
)

router = APIRouter(
    prefix="/tank-design",
    tags=["Tank Design"],
)


@router.post(
    "/calculate",
    response_model=TankResult,
)
def calculate(data: TankInput):
    return calculate_tank(data)