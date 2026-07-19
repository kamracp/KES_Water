from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class WaterAccountingZoneType(StrEnum):
    PRODUCTION = "PRODUCTION"
    UTILITY = "UTILITY"
    DOMESTIC = "DOMESTIC"
    COOLING = "COOLING"
    BOILER = "BOILER"
    WATER_TREATMENT = "WATER_TREATMENT"
    WASTEWATER_TREATMENT = "WASTEWATER_TREATMENT"
    REUSE_RECYCLE = "REUSE_RECYCLE"
    WAREHOUSE = "WAREHOUSE"
    ADMINISTRATION = "ADMINISTRATION"
    RESIDENTIAL = "RESIDENTIAL"
    OTHER = "OTHER"


class WaterBalanceFrequency(StrEnum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"


class WaterAccountingZoneBase(BaseModel):
    organization_id: int = Field(gt=0)
    plant_id: int = Field(gt=0)
    parent_zone_id: int | None = Field(default=None, gt=0)

    zone_code: str = Field(min_length=2, max_length=30)
    zone_name: str = Field(min_length=2, max_length=150)
    zone_type: WaterAccountingZoneType

    audit_boundary_description: str | None = None
    process_description: str | None = None

    elevation_m: Decimal | None = Field(
        default=None,
        max_digits=10,
        decimal_places=3,
    )
    design_water_demand_m3_day: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=14,
        decimal_places=3,
    )

    baseline_start_date: date | None = None
    baseline_end_date: date | None = None
    baseline_consumption_m3: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=16,
        decimal_places=3,
    )

    water_balance_frequency: WaterBalanceFrequency = (
        WaterBalanceFrequency.MONTHLY
    )
    metering_coverage_percent: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )
    audit_tolerance_percent: Decimal = Field(
        default=Decimal("5.00"),
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )

    responsible_person: str | None = Field(
        default=None,
        max_length=150,
    )
    cost_center: str | None = Field(
        default=None,
        max_length=50,
    )

    is_audit_boundary: bool = True
    is_hydraulic_zone: bool = False
    is_active: bool = True

    @field_validator("zone_code")
    @classmethod
    def normalize_zone_code(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator(
        "zone_name",
        "audit_boundary_description",
        "process_description",
        "responsible_person",
        "cost_center",
    )
    @classmethod
    def strip_text_values(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        return cleaned_value or None

    @model_validator(mode="after")
    def validate_baseline_dates(self) -> WaterAccountingZoneBase:
        if (
            self.baseline_start_date is not None
            and self.baseline_end_date is not None
            and self.baseline_end_date < self.baseline_start_date
        ):
            raise ValueError(
                "baseline_end_date cannot be earlier than "
                "baseline_start_date."
            )

        return self


class WaterAccountingZoneCreate(WaterAccountingZoneBase):
    pass


class WaterAccountingZoneUpdate(BaseModel):
    organization_id: int | None = Field(default=None, gt=0)
    plant_id: int | None = Field(default=None, gt=0)
    parent_zone_id: int | None = Field(default=None, gt=0)

    zone_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
    )
    zone_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    zone_type: WaterAccountingZoneType | None = None

    audit_boundary_description: str | None = None
    process_description: str | None = None

    elevation_m: Decimal | None = Field(
        default=None,
        max_digits=10,
        decimal_places=3,
    )
    design_water_demand_m3_day: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=14,
        decimal_places=3,
    )

    baseline_start_date: date | None = None
    baseline_end_date: date | None = None
    baseline_consumption_m3: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=16,
        decimal_places=3,
    )

    water_balance_frequency: WaterBalanceFrequency | None = None
    metering_coverage_percent: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )
    audit_tolerance_percent: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )

    responsible_person: str | None = Field(
        default=None,
        max_length=150,
    )
    cost_center: str | None = Field(
        default=None,
        max_length=50,
    )

    is_audit_boundary: bool | None = None
    is_hydraulic_zone: bool | None = None
    is_active: bool | None = None

    @field_validator("zone_code")
    @classmethod
    def normalize_zone_code(
        cls,
        value: str | None,
    ) -> str | None:
        return value.strip().upper() if value is not None else None

    @field_validator(
        "zone_name",
        "audit_boundary_description",
        "process_description",
        "responsible_person",
        "cost_center",
    )
    @classmethod
    def strip_text_values(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        return cleaned_value or None

    @model_validator(mode="after")
    def validate_baseline_dates(self) -> WaterAccountingZoneUpdate:
        if (
            self.baseline_start_date is not None
            and self.baseline_end_date is not None
            and self.baseline_end_date < self.baseline_start_date
        ):
            raise ValueError(
                "baseline_end_date cannot be earlier than "
                "baseline_start_date."
            )

        return self


class WaterAccountingZoneResponse(WaterAccountingZoneBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
