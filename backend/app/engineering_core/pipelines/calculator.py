from pydantic import BaseModel
import math


class PipelineInput(BaseModel):
    flow_m3_hr: float
    velocity_m_s: float


class PipelineResult(BaseModel):
    flow_lps: float
    diameter_mm: float
    nominal_diameter_mm: int


STANDARD_PIPE_SIZES = [
    15, 20, 25, 32, 40, 50, 65, 80,
    100, 125, 150, 200, 250, 300,
    350, 400, 450, 500, 600
]


def nearest_pipe_size(diameter_mm: float) -> int:
    for size in STANDARD_PIPE_SIZES:
        if size >= diameter_mm:
            return size
    return STANDARD_PIPE_SIZES[-1]


def calculate_pipeline(data: PipelineInput) -> PipelineResult:
    flow_lps = data.flow_m3_hr / 3.6
    flow_m3_s = data.flow_m3_hr / 3600

    diameter_m = math.sqrt(
        (4 * flow_m3_s) / (math.pi * data.velocity_m_s)
    )

    diameter_mm = diameter_m * 1000

    return PipelineResult(
        flow_lps=round(flow_lps, 2),
        diameter_mm=round(diameter_mm, 2),
        nominal_diameter_mm=nearest_pipe_size(diameter_mm),
    )