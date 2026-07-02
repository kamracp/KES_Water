from pydantic import BaseModel


class WaterBalanceInput(BaseModel):
    fresh_water_kl_day: float
    recycled_water_kl_day: float
    process_use_kl_day: float
    domestic_use_kl_day: float
    losses_kl_day: float


class WaterBalanceResult(BaseModel):
    total_input_kl_day: float
    total_use_kl_day: float
    water_loss_percent: float
    recycle_percent: float
    balance_status: str


def calculate_water_balance(data: WaterBalanceInput) -> WaterBalanceResult:
    total_input = data.fresh_water_kl_day + data.recycled_water_kl_day
    total_use = data.process_use_kl_day + data.domestic_use_kl_day + data.losses_kl_day

    loss_percent = (data.losses_kl_day / total_input) * 100 if total_input else 0
    recycle_percent = (data.recycled_water_kl_day / total_input) * 100 if total_input else 0

    difference = abs(total_input - total_use)
    status = "BALANCED" if difference <= 0.05 * total_input else "IMBALANCED"

    return WaterBalanceResult(
        total_input_kl_day=round(total_input, 2),
        total_use_kl_day=round(total_use, 2),
        water_loss_percent=round(loss_percent, 2),
        recycle_percent=round(recycle_percent, 2),
        balance_status=status,
    )
