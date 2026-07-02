from fastapi import APIRouter

from app.engineering_core.friction_loss.calculator import (
    FrictionLossCalculator,
)
from app.schemas.friction_loss import (
    FrictionLossRequest,
    FrictionLossResponse,
)

router = APIRouter(
    prefix="/friction-loss",
    tags=["Friction Loss Calculator"],
)


@router.post(
    "/calculate",
    response_model=FrictionLossResponse,
    summary="Calculate Pipe Friction Loss",
)
def calculate_friction_loss(
    request: FrictionLossRequest,
) -> FrictionLossResponse:
    """
    Calculate friction loss in a pipeline using the Darcy–Weisbach equation.

    Inputs:
    - Flow Rate (m³/hr)
    - Pipe Diameter (mm)
    - Pipe Length (m)
    - Pipe Roughness (mm)
    - Fluid Density (kg/m³)
    - Dynamic Viscosity (Pa·s)

    Returns:
    - Velocity
    - Reynolds Number
    - Flow Regime
    - Relative Roughness
    - Friction Factor
    - Friction Loss (m)
    - Pressure Loss (kPa)
    """
    return FrictionLossCalculator.calculate(request)