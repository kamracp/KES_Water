from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.engineering_core.water_balance.engine import WaterBalanceStatus


WaterVolume = Annotated[
    Decimal,
    Field(
        ge=0,
        max_digits=18,
        decimal_places=3,
        allow_inf_nan=False,
    ),
]

NonNegativeDecimal = Annotated[
    Decimal,
    Field(
        ge=0,
        allow_inf_nan=False,
    ),
]

FiniteDecimal = Annotated[
    Decimal,
    Field(
        allow_inf_nan=False,
    ),
]

Percentage = Annotated[
    Decimal,
    Field(
        ge=0,
        le=100,
        allow_inf_nan=False,
    ),
]


class WaterBalanceCalculationRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    organization_id: int = Field(gt=0)
    plant_id: int = Field(gt=0)
    water_accounting_zone_id: int = Field(gt=0)

    period_start: date
    period_end: date

    external_fresh_water_m3: WaterVolume = Decimal("0")
    external_reclaimed_water_m3: WaterVolume = Decimal("0")
    interzone_inflow_m3: WaterVolume = Decimal("0")

    wastewater_discharge_m3: WaterVolume = Decimal("0")
    interzone_outflow_m3: WaterVolume = Decimal("0")
    evaporation_m3: WaterVolume = Decimal("0")
    product_incorporation_m3: WaterVolume = Decimal("0")
    other_consumptive_use_m3: WaterVolume = Decimal("0")

    opening_storage_m3: WaterVolume = Decimal("0")
    closing_storage_m3: WaterVolume = Decimal("0")

    internal_reuse_m3: WaterVolume = Decimal("0")

    calculation_reference: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    notes: str | None = Field(
        default=None,
        min_length=1,
        max_length=1000,
    )

    @model_validator(mode="after")
    def validate_audit_period(self) -> Self:
        if self.period_end < self.period_start:
            raise ValueError(
                "period_end must be greater than or equal to period_start."
            )

        return self


class WaterBalanceCalculationResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )

    organization_id: int
    plant_id: int
    water_accounting_zone_id: int

    period_start: date
    period_end: date
    period_days: int = Field(gt=0)

    volume_unit: Literal["m3"] = "m3"
    calculation_basis: Literal["BOUNDARY_VOLUME"] = "BOUNDARY_VOLUME"

    total_external_inflow_m3: NonNegativeDecimal
    total_boundary_inflow_m3: NonNegativeDecimal
    total_consumptive_use_m3: NonNegativeDecimal
    total_boundary_outflow_m3: NonNegativeDecimal
    net_storage_change_m3: FiniteDecimal

    signed_balance_error_m3: FiniteDecimal
    absolute_balance_error_m3: NonNegativeDecimal
    balance_error_percent: NonNegativeDecimal | None
    balance_closure_percent: FiniteDecimal | None

    unaccounted_water_m3: NonNegativeDecimal
    over_accounted_water_m3: NonNegativeDecimal

    gross_water_demand_m3: NonNegativeDecimal
    internal_reuse_percent: Percentage | None

    audit_tolerance_percent: Percentage
    status: WaterBalanceStatus

    calculation_reference: str | None = None
    notes: str | None = None

    assumptions: list[str] = Field(default_factory=list)
    calculated_at: datetime