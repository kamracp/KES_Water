from datetime import datetime, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.engineering_core.water_balance.engine import (
    WaterBalanceStatus,
)
from app.schemas.water_balance import (
    WaterBalanceCalculationRequest,
    WaterBalanceCalculationResponse,
)


def valid_request_data() -> dict:
    return {
        "organization_id": 2,
        "plant_id": 1,
        "water_accounting_zone_id": 1,
        "period_start": "2026-07-01",
        "period_end": "2026-07-31",
        "external_fresh_water_m3": "100.000",
        "external_reclaimed_water_m3": "20.000",
        "wastewater_discharge_m3": "50.000",
        "evaporation_m3": "30.000",
        "product_incorporation_m3": "10.000",
        "other_consumptive_use_m3": "10.000",
        "opening_storage_m3": "10.000",
        "closing_storage_m3": "30.000",
        "internal_reuse_m3": "40.000",
        "calculation_reference": "KESW-S3-M1-TEST",
        "notes": "Schema regression test.",
    }


def test_valid_request_is_parsed() -> None:
    request = WaterBalanceCalculationRequest(
        **valid_request_data()
    )

    assert request.organization_id == 2
    assert request.plant_id == 1
    assert request.water_accounting_zone_id == 1
    assert request.external_fresh_water_m3 == Decimal("100.000")
    assert request.period_start.isoformat() == "2026-07-01"
    assert request.period_end.isoformat() == "2026-07-31"


def test_volume_defaults_are_zero() -> None:
    request = WaterBalanceCalculationRequest(
        organization_id=2,
        plant_id=1,
        water_accounting_zone_id=1,
        period_start="2026-07-01",
        period_end="2026-07-31",
    )

    assert request.external_fresh_water_m3 == Decimal("0")
    assert request.internal_reuse_m3 == Decimal("0")
    assert request.opening_storage_m3 == Decimal("0")
    assert request.closing_storage_m3 == Decimal("0")


def test_period_end_before_start_is_rejected() -> None:
    data = valid_request_data()
    data["period_start"] = "2026-07-31"
    data["period_end"] = "2026-07-01"

    with pytest.raises(
        ValidationError,
        match="period_end must be greater",
    ):
        WaterBalanceCalculationRequest(**data)


def test_same_day_period_is_allowed() -> None:
    data = valid_request_data()
    data["period_start"] = "2026-07-19"
    data["period_end"] = "2026-07-19"

    request = WaterBalanceCalculationRequest(**data)

    assert request.period_start == request.period_end


@pytest.mark.parametrize(
    "field_name",
    [
        "organization_id",
        "plant_id",
        "water_accounting_zone_id",
    ],
)
def test_non_positive_entity_id_is_rejected(
    field_name: str,
) -> None:
    data = valid_request_data()
    data[field_name] = 0

    with pytest.raises(ValidationError):
        WaterBalanceCalculationRequest(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "external_fresh_water_m3",
        "wastewater_discharge_m3",
        "internal_reuse_m3",
    ],
)
def test_negative_volume_is_rejected(
    field_name: str,
) -> None:
    data = valid_request_data()
    data[field_name] = "-0.001"

    with pytest.raises(ValidationError):
        WaterBalanceCalculationRequest(**data)


def test_more_than_three_decimal_places_is_rejected() -> None:
    data = valid_request_data()
    data["external_fresh_water_m3"] = "100.0001"

    with pytest.raises(ValidationError):
        WaterBalanceCalculationRequest(**data)


@pytest.mark.parametrize(
    "value",
    [
        "NaN",
        "Infinity",
        "-Infinity",
    ],
)
def test_non_finite_volume_is_rejected(
    value: str,
) -> None:
    data = valid_request_data()
    data["external_fresh_water_m3"] = value

    with pytest.raises(ValidationError):
        WaterBalanceCalculationRequest(**data)


def test_unknown_field_is_rejected() -> None:
    data = valid_request_data()
    data["unknown_water_field"] = "10"

    with pytest.raises(ValidationError):
        WaterBalanceCalculationRequest(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "calculation_reference",
        "notes",
    ],
)
def test_blank_optional_text_is_rejected(
    field_name: str,
) -> None:
    data = valid_request_data()
    data[field_name] = "   "

    with pytest.raises(ValidationError):
        WaterBalanceCalculationRequest(**data)


def test_response_schema_serializes_engineering_result() -> None:
    response = WaterBalanceCalculationResponse(
        organization_id=2,
        plant_id=1,
        water_accounting_zone_id=1,
        period_start="2026-07-01",
        period_end="2026-07-31",
        period_days=31,
        total_external_inflow_m3=Decimal("120"),
        total_boundary_inflow_m3=Decimal("120"),
        total_consumptive_use_m3=Decimal("50"),
        total_boundary_outflow_m3=Decimal("100"),
        net_storage_change_m3=Decimal("20"),
        signed_balance_error_m3=Decimal("0"),
        absolute_balance_error_m3=Decimal("0"),
        balance_error_percent=Decimal("0"),
        balance_closure_percent=Decimal("100"),
        unaccounted_water_m3=Decimal("0"),
        over_accounted_water_m3=Decimal("0"),
        gross_water_demand_m3=Decimal("160"),
        internal_reuse_percent=Decimal("25"),
        audit_tolerance_percent=Decimal("5"),
        status=WaterBalanceStatus.BALANCED,
        calculated_at=datetime.now(timezone.utc),
    )

    serialized = response.model_dump(mode="json")

    assert serialized["volume_unit"] == "m3"
    assert serialized["calculation_basis"] == "BOUNDARY_VOLUME"
    assert serialized["status"] == "BALANCED"
    assert serialized["total_external_inflow_m3"] == "120"
    assert serialized["internal_reuse_percent"] == "25"