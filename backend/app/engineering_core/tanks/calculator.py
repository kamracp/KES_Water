from pydantic import BaseModel


class TankInput(BaseModel):
    length_m: float
    width_m: float
    water_depth_m: float
    freeboard_m: float = 0.3


class TankResult(BaseModel):
    gross_volume_m3: float
    effective_volume_m3: float
    gross_volume_liters: float
    effective_volume_liters: float


def calculate_tank(data: TankInput) -> TankResult:

    gross_volume = (
        data.length_m *
        data.width_m *
        data.water_depth_m
    )

    effective_depth = data.water_depth_m - data.freeboard_m

    if effective_depth < 0:
        effective_depth = 0

    effective_volume = (
        data.length_m *
        data.width_m *
        effective_depth
    )

    return TankResult(
        gross_volume_m3=round(gross_volume, 2),
        effective_volume_m3=round(effective_volume, 2),
        gross_volume_liters=round(gross_volume * 1000, 0),
        effective_volume_liters=round(effective_volume * 1000, 0),
    )