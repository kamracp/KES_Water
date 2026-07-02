from pydantic import BaseModel, Field


class FrictionLossRequest(BaseModel):
    flow_rate_m3_hr: float = Field(..., gt=0)
    pipe_diameter_mm: float = Field(..., gt=0)
    pipe_length_m: float = Field(..., gt=0)

    pipe_roughness_mm: float = Field(
        default=0.045,
        gt=0,
        description="Absolute roughness of pipe"
    )

    fluid_density_kg_m3: float = Field(
        default=1000.0,
        gt=0
    )

    dynamic_viscosity_pa_s: float = Field(
        default=0.001,
        gt=0
    )


class FrictionLossResponse(BaseModel):
    velocity_m_s: float

    reynolds_number: float

    flow_regime: str

    relative_roughness: float

    friction_factor: float

    friction_loss_m: float

    pressure_loss_kpa: float