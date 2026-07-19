from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.engineering_core.water_balance.engine import (
    WaterBalanceStatus,
)
from app.schemas.water_balance import (
    WaterBalanceCalculationRequest,
)
from app.services.water_balance_service import (
    WaterBalanceCalculationService,
)


def make_payload(
    **overrides,
) -> WaterBalanceCalculationRequest:
    data = {
        "organization_id": 2,
        "plant_id": 1,
        "water_accounting_zone_id": 1,
        "period_start": "2026-07-01",
        "period_end": "2026-07-31",
        "external_fresh_water_m3": "100",
        "wastewater_discharge_m3": "96",
        "calculation_reference": "SERVICE-TEST",
    }
    data.update(overrides)
    return WaterBalanceCalculationRequest(**data)


def build_service() -> tuple:
    service = WaterBalanceCalculationService(MagicMock())

    service.organization_repository = MagicMock()
    service.plant_repository = MagicMock()
    service.zone_repository = MagicMock()

    organization = SimpleNamespace(
        id=2,
        is_active=True,
    )

    plant = SimpleNamespace(
        id=1,
        organization_id=2,
        is_active=True,
    )

    zone = SimpleNamespace(
        id=1,
        organization_id=2,
        plant_id=1,
        audit_tolerance_percent=Decimal("5"),
        is_active=True,
    )

    service.organization_repository.get_by_id.return_value = (
        organization
    )
    service.plant_repository.get_by_id.return_value = plant
    service.zone_repository.get_by_id.return_value = zone

    return service, organization, plant, zone


def test_service_uses_zone_tolerance() -> None:
    service, _, _, zone = build_service()

    zone.audit_tolerance_percent = Decimal("5")

    result = service.calculate(make_payload())

    assert result.audit_tolerance_percent == Decimal("5")
    assert result.balance_error_percent == Decimal("4")
    assert result.status == WaterBalanceStatus.BALANCED
    assert result.period_days == 31
    assert result.organization_id == 2
    assert result.plant_id == 1
    assert result.water_accounting_zone_id == 1
    assert result.assumptions


def test_stricter_zone_tolerance_changes_status() -> None:
    service, _, _, zone = build_service()

    zone.audit_tolerance_percent = Decimal("3")

    result = service.calculate(make_payload())

    assert result.balance_error_percent == Decimal("4")
    assert result.audit_tolerance_percent == Decimal("3")
    assert result.status == WaterBalanceStatus.IMBALANCED


def test_missing_organization_returns_404() -> None:
    service, _, _, _ = build_service()
    service.organization_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.calculate(make_payload())

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Organization not found."


def test_missing_plant_returns_404() -> None:
    service, _, _, _ = build_service()
    service.plant_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.calculate(make_payload())

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Plant not found."


def test_missing_zone_returns_404() -> None:
    service, _, _, _ = build_service()
    service.zone_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.calculate(make_payload())

    assert exc_info.value.status_code == 404
    assert (
        exc_info.value.detail
        == "Water Accounting Zone not found."
    )


def test_plant_organization_mismatch_returns_400() -> None:
    service, _, plant, _ = build_service()
    plant.organization_id = 999

    with pytest.raises(HTTPException) as exc_info:
        service.calculate(make_payload())

    assert exc_info.value.status_code == 400
    assert (
        exc_info.value.detail
        == "Plant does not belong to the specified organization."
    )


@pytest.mark.parametrize(
    ("zone_organization_id", "zone_plant_id"),
    [
        (999, 1),
        (2, 999),
    ],
)
def test_zone_ownership_mismatch_returns_400(
    zone_organization_id: int,
    zone_plant_id: int,
) -> None:
    service, _, _, zone = build_service()
    zone.organization_id = zone_organization_id
    zone.plant_id = zone_plant_id

    with pytest.raises(HTTPException) as exc_info:
        service.calculate(make_payload())

    assert exc_info.value.status_code == 400
    assert (
        exc_info.value.detail
        == (
            "Water Accounting Zone does not belong to the "
            "specified Organization and Plant."
        )
    )


@pytest.mark.parametrize(
    ("entity_name", "expected_detail"),
    [
        ("organization", "Organization is inactive."),
        ("plant", "Plant is inactive."),
        ("zone", "Water Accounting Zone is inactive."),
    ],
)
def test_inactive_entity_returns_409(
    entity_name: str,
    expected_detail: str,
) -> None:
    service, organization, plant, zone = build_service()

    entities = {
        "organization": organization,
        "plant": plant,
        "zone": zone,
    }
    entities[entity_name].is_active = False

    with pytest.raises(HTTPException) as exc_info:
        service.calculate(make_payload())

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == expected_detail


def test_invalid_database_tolerance_returns_422() -> None:
    service, _, _, zone = build_service()
    zone.audit_tolerance_percent = Decimal("-1")

    with pytest.raises(HTTPException) as exc_info:
        service.calculate(make_payload())

    assert exc_info.value.status_code == 422
    assert (
        exc_info.value.detail
        == "audit_tolerance_percent must be between 0 and 100."
    )


def test_reference_and_notes_are_preserved() -> None:
    service, _, _, _ = build_service()

    result = service.calculate(
        make_payload(
            calculation_reference="WB-JUL-2026",
            notes="Monthly verified meter data.",
        )
    )

    assert result.calculation_reference == "WB-JUL-2026"
    assert result.notes == "Monthly verified meter data."