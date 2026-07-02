from pydantic import BaseModel
import math


class FrictionLossInput(BaseModel):
    flow_m3_hr: float
    pipe_diameter_mm: float
    pipe_length_m: float
    hazen_williams_c: float = 130


class FrictionLossResult(BaseModel):
    flow_lps: float
    velocity_m_s: float
    friction_loss_m: float
    friction_loss_m_per_100m: float


def calculate_friction_loss(data: FrictionLossInput) -> FrictionLossResult:
    flow_m3_s = data.flow_m3_hr / 3600
    flow_lps = data.flow_m3_hr / 3.6
    diameter_m = data.pipe_diameter_mm / 1000

    area_m2 = math.pi * diameter_m**2 / 4
    velocity_m_s = flow_m3_s / area_m2

    # Hazen-Williams formula, SI units
    friction_loss_m = (
        10.67
        * data.pipe_length_m
        * flow_m3_s**1.852
        / (
            data.hazen_williams_c**1.852
            * diameter_m**4.87
        )
    )

    return FrictionLossResult(
        flow_lps=round(flow_lps, 2),
        velocity_m_s=round(velocity_m_s, 2),
        friction_loss_m=round(friction_loss_m, 2),
        friction_loss_m_per_100m=round(
            friction_loss_m / data.pipe_length_m * 100,
            2,
        ),
    )