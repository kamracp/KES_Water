from pydantic import BaseModel


class PumpHeadInput(BaseModel):
    suction_static_head_m: float
    discharge_static_head_m: float
    friction_loss_m: float
    fitting_loss_m: float
    equipment_loss_m: float = 0
    safety_margin_percent: float = 10


class PumpHeadResult(BaseModel):
    static_head_m: float
    total_loss_m: float
    head_before_margin_m: float
    safety_margin_m: float
    total_dynamic_head_m: float


def calculate_pump_head(data: PumpHeadInput) -> PumpHeadResult:
    static_head = data.discharge_static_head_m - data.suction_static_head_m

    total_loss = (
        data.friction_loss_m
        + data.fitting_loss_m
        + data.equipment_loss_m
    )

    head_before_margin = static_head + total_loss
    safety_margin = head_before_margin * data.safety_margin_percent / 100
    total_dynamic_head = head_before_margin + safety_margin

    return PumpHeadResult(
        static_head_m=round(static_head, 2),
        total_loss_m=round(total_loss, 2),
        head_before_margin_m=round(head_before_margin, 2),
        safety_margin_m=round(safety_margin, 2),
        total_dynamic_head_m=round(total_dynamic_head, 2),
    )