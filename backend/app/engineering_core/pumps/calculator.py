from pydantic import BaseModel


class PumpSelectionInput(BaseModel):
    flow_m3_hr: float
    total_head_m: float
    pump_efficiency_percent: float = 70
    motor_efficiency_percent: float = 90
    service_factor: float = 1.15


class PumpSelectionResult(BaseModel):
    flow_lps: float
    hydraulic_power_kw: float
    shaft_power_kw: float
    motor_input_power_kw: float
    recommended_motor_kw: float
    pump_category: str


STANDARD_MOTORS_KW = [
    0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3.7, 5.5, 7.5, 11,
    15, 18.5, 22, 30, 37, 45, 55, 75, 90, 110, 132, 160, 200
]


def select_standard_motor(required_kw: float) -> float:
    for motor_kw in STANDARD_MOTORS_KW:
        if motor_kw >= required_kw:
            return motor_kw
    return STANDARD_MOTORS_KW[-1]


def calculate_pump_selection(data: PumpSelectionInput) -> PumpSelectionResult:
    flow_lps = data.flow_m3_hr / 3.6

    hydraulic_power_kw = (1000 * 9.81 * flow_lps / 1000 * data.total_head_m) / 1000

    pump_eff = data.pump_efficiency_percent / 100
    motor_eff = data.motor_efficiency_percent / 100

    shaft_power_kw = hydraulic_power_kw / pump_eff if pump_eff else 0
    motor_input_power_kw = shaft_power_kw / motor_eff if motor_eff else 0

    required_motor_kw = shaft_power_kw * data.service_factor
    recommended_motor_kw = select_standard_motor(required_motor_kw)

    if data.total_head_m <= 30:
        category = "Low Head Pump"
    elif data.total_head_m <= 80:
        category = "Medium Head Pump"
    else:
        category = "High Head Pump"

    return PumpSelectionResult(
        flow_lps=round(flow_lps, 2),
        hydraulic_power_kw=round(hydraulic_power_kw, 2),
        shaft_power_kw=round(shaft_power_kw, 2),
        motor_input_power_kw=round(motor_input_power_kw, 2),
        recommended_motor_kw=recommended_motor_kw,
        pump_category=category,
    )
