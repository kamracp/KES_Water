import math

from app.schemas.friction_loss import (
    FrictionLossRequest,
    FrictionLossResponse,
)


class FrictionLossCalculator:
    """
    Darcy–Weisbach Friction Loss Calculator

    Supports:
    - Laminar Flow
    - Transitional Flow
    - Turbulent Flow
    """

    GRAVITY = 9.81

    @staticmethod
    def calculate(request: FrictionLossRequest) -> FrictionLossResponse:

        # -----------------------------
        # Unit Conversions
        # -----------------------------

        flow_rate_m3_s = request.flow_rate_m3_hr / 3600.0

        diameter_m = request.pipe_diameter_mm / 1000.0

        roughness_m = request.pipe_roughness_mm / 1000.0

        # -----------------------------
        # Velocity
        # -----------------------------

        area = math.pi * (diameter_m ** 2) / 4.0

        velocity = flow_rate_m3_s / area

        # -----------------------------
        # Reynolds Number
        # -----------------------------

        reynolds = (
            request.fluid_density_kg_m3
            * velocity
            * diameter_m
            / request.dynamic_viscosity_pa_s
        )

        # -----------------------------
        # Relative Roughness
        # -----------------------------

        relative_roughness = roughness_m / diameter_m

        # -----------------------------
        # Friction Factor
        # -----------------------------

        if reynolds < 2300:

            flow_regime = "Laminar"

            friction_factor = 64.0 / reynolds

        elif reynolds <= 4000:

            flow_regime = "Transitional"

            # Smooth interpolation between laminar and turbulent
            f_laminar = 64.0 / reynolds

            f_turbulent = 0.25 / (
                math.log10(
                    (relative_roughness / 3.7)
                    + (5.74 / (reynolds ** 0.9))
                )
                ** 2
            )

            interpolation = (reynolds - 2300.0) / (4000.0 - 2300.0)

            friction_factor = (
                f_laminar
                + interpolation * (f_turbulent - f_laminar)
            )

        else:

            flow_regime = "Turbulent"

            # Swamee–Jain Equation
            friction_factor = 0.25 / (
                math.log10(
                    (relative_roughness / 3.7)
                    + (5.74 / (reynolds ** 0.9))
                )
                ** 2
            )

        # -----------------------------
        # Darcy–Weisbach Equation
        # -----------------------------

        friction_loss = (
            friction_factor
            * (request.pipe_length_m / diameter_m)
            * (velocity ** 2)
            / (2 * FrictionLossCalculator.GRAVITY)
        )

        pressure_loss_pa = (
            request.fluid_density_kg_m3
            * FrictionLossCalculator.GRAVITY
            * friction_loss
        )

        pressure_loss_kpa = pressure_loss_pa / 1000.0

        return FrictionLossResponse(
            velocity_m_s=round(velocity, 4),
            reynolds_number=round(reynolds, 2),
            flow_regime=flow_regime,
            relative_roughness=round(relative_roughness, 6),
            friction_factor=round(friction_factor, 6),
            friction_loss_m=round(friction_loss, 4),
            pressure_loss_kpa=round(pressure_loss_kpa, 4),
        )