from datetime import date, datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api import engineering_water_balance
from app.database.session import get_db
from app.engineering_core.water_balance.engine import (
    WaterBalanceStatus,
)
from app.main import app
from app.schemas.water_balance import (
    WaterBalanceCalculationRequest,
    WaterBalanceCalculationResponse,
)


class FakeWaterBalanceCalculationService:
    last_payload: WaterBalanceCalculationRequest | None = None

    def __init__(self, db):
        self.db = db

    def calculate(
        self,
        payload: WaterBalanceCalculationRequest,
    ) -> WaterBalanceCalculationResponse:
        type(self).last_payload = payload

        if payload.calculation_reference == "FORCE-404":
            raise HTTPException(
                status_code=404,
                detail="Water Accounting Zone not found.",
            )

        return WaterBalanceCalculationResponse(
            organization_id=payload.organization_id,
            plant_id=payload.plant_id,
            water_accounting_zone_id=(
                payload.water_accounting_zone_id
            ),
            period_start=payload.period_start,
            period_end=payload.period_end,
            period_days=(
                payload.period_end - payload.period_start
            ).days + 1,
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
            calculation_reference=(
                payload.calculation_reference
            ),
            notes=payload.notes,
            assumptions=[
                "All input volumes cover the same audit period.",
            ],
            calculated_at=datetime(
                2026,
                7,
                19,
                12,
                0,
                tzinfo=timezone.utc,
            ),
        )


def valid_payload() -> dict:
    return {
        "organization_id": 2,
        "plant_id": 1,
        "water_accounting_zone_id": 1,
        "period_start": "2026-07-01",
        "period_end": "2026-07-31",
        "external_fresh_water_m3": 100,
        "external_reclaimed_water_m3": 20,
        "wastewater_discharge_m3": 50,
        "evaporation_m3": 30,
        "product_incorporation_m3": 10,
        "other_consumptive_use_m3": 10,
        "opening_storage_m3": 10,
        "closing_storage_m3": 30,
        "internal_reuse_m3": 40,
        "calculation_reference": "API-TEST-001",
        "notes": "API regression test.",
    }


@pytest.fixture
def client(
    monkeypatch: pytest.MonkeyPatch,
):
    def override_get_db():
        yield MagicMock()

    monkeypatch.setattr(
        engineering_water_balance,
        "WaterBalanceCalculationService",
        FakeWaterBalanceCalculationService,
    )

    app.dependency_overrides[get_db] = override_get_db
    FakeWaterBalanceCalculationService.last_payload = None

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_calculate_endpoint_returns_balanced_result(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/engineering/water-balance/calculate",
        json=valid_payload(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["organization_id"] == 2
    assert data["plant_id"] == 1
    assert data["water_accounting_zone_id"] == 1
    assert data["period_days"] == 31
    assert data["volume_unit"] == "m3"
    assert data["calculation_basis"] == "BOUNDARY_VOLUME"
    assert data["total_boundary_inflow_m3"] == "120"
    assert data["signed_balance_error_m3"] == "0"
    assert data["internal_reuse_percent"] == "25"
    assert data["audit_tolerance_percent"] == "5"
    assert data["status"] == "BALANCED"

    received = (
        FakeWaterBalanceCalculationService.last_payload
    )

    assert received is not None
    assert received.period_start == date(2026, 7, 1)
    assert received.external_fresh_water_m3 == Decimal("100")


def test_missing_required_context_returns_422(
    client: TestClient,
) -> None:
    payload = valid_payload()
    payload.pop("water_accounting_zone_id")

    response = client.post(
        "/api/v1/engineering/water-balance/calculate",
        json=payload,
    )

    assert response.status_code == 422


def test_invalid_period_returns_422(
    client: TestClient,
) -> None:
    payload = valid_payload()
    payload["period_start"] = "2026-07-31"
    payload["period_end"] = "2026-07-01"

    response = client.post(
        "/api/v1/engineering/water-balance/calculate",
        json=payload,
    )

    assert response.status_code == 422


def test_negative_volume_returns_422(
    client: TestClient,
) -> None:
    payload = valid_payload()
    payload["external_fresh_water_m3"] = -1

    response = client.post(
        "/api/v1/engineering/water-balance/calculate",
        json=payload,
    )

    assert response.status_code == 422


def test_unknown_field_returns_422(
    client: TestClient,
) -> None:
    payload = valid_payload()
    payload["unknown_field"] = 10

    response = client.post(
        "/api/v1/engineering/water-balance/calculate",
        json=payload,
    )

    assert response.status_code == 422


def test_service_http_error_is_preserved(
    client: TestClient,
) -> None:
    payload = valid_payload()
    payload["calculation_reference"] = "FORCE-404"

    response = client.post(
        "/api/v1/engineering/water-balance/calculate",
        json=payload,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Water Accounting Zone not found."
    }


def test_openapi_contains_enterprise_water_balance_route(
    client: TestClient,
) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200

    paths = response.json()["paths"]

    assert (
        "/api/v1/engineering/water-balance/calculate"
        in paths
    )