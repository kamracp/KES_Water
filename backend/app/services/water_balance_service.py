from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Final

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.engineering_core.water_balance.engine import (
    WaterBalanceDomainError,
    WaterBalanceInputs,
    calculate_water_balance,
)
from app.models.organization import Organization
from app.models.plant import Plant
from app.models.water_accounting_zone import WaterAccountingZone
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.plant_repository import PlantRepository
from app.repositories.water_accounting_zone_repository import (
    WaterAccountingZoneRepository,
)
from app.schemas.water_balance import (
    WaterBalanceCalculationRequest,
    WaterBalanceCalculationResponse,
)


WATER_BALANCE_ASSUMPTIONS: Final[tuple[str, ...]] = (
    "All input volumes cover the same audit period.",
    "All water volumes use cubic metres.",
    "Internal reuse is excluded from boundary inflow.",
    "Internal reuse is used only for the circularity KPI.",
    "Positive signed error represents unaccounted water.",
    "Negative signed error represents over-accounted water.",
    "Audit tolerance is taken from the Water Accounting Zone.",
)


class WaterBalanceCalculationService:
    def __init__(self, db: Session):
        self.organization_repository = OrganizationRepository(db)
        self.plant_repository = PlantRepository(db)
        self.zone_repository = WaterAccountingZoneRepository(db)

    def calculate(
        self,
        payload: WaterBalanceCalculationRequest,
    ) -> WaterBalanceCalculationResponse:
        organization = self._get_organization(
            payload.organization_id
        )

        plant = self._get_plant(payload.plant_id)
        self._ensure_plant_ownership(
            plant,
            organization.id,
        )

        zone = self._get_zone(
            payload.water_accounting_zone_id
        )
        self._ensure_zone_ownership(
            zone,
            organization.id,
            plant.id,
        )

        self._ensure_active(
            organization=organization,
            plant=plant,
            zone=zone,
        )

        try:
            domain_input = WaterBalanceInputs(
                external_fresh_water_m3=(
                    payload.external_fresh_water_m3
                ),
                external_reclaimed_water_m3=(
                    payload.external_reclaimed_water_m3
                ),
                interzone_inflow_m3=(
                    payload.interzone_inflow_m3
                ),
                wastewater_discharge_m3=(
                    payload.wastewater_discharge_m3
                ),
                interzone_outflow_m3=(
                    payload.interzone_outflow_m3
                ),
                evaporation_m3=payload.evaporation_m3,
                product_incorporation_m3=(
                    payload.product_incorporation_m3
                ),
                other_consumptive_use_m3=(
                    payload.other_consumptive_use_m3
                ),
                opening_storage_m3=(
                    payload.opening_storage_m3
                ),
                closing_storage_m3=(
                    payload.closing_storage_m3
                ),
                internal_reuse_m3=payload.internal_reuse_m3,
                audit_tolerance_percent=(
                    zone.audit_tolerance_percent
                ),
            )

            result = calculate_water_balance(domain_input)
        except WaterBalanceDomainError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

        period_days = (
            payload.period_end - payload.period_start
        ).days + 1

        return WaterBalanceCalculationResponse(
            organization_id=organization.id,
            plant_id=plant.id,
            water_accounting_zone_id=zone.id,
            period_start=payload.period_start,
            period_end=payload.period_end,
            period_days=period_days,
            calculation_reference=(
                payload.calculation_reference
            ),
            notes=payload.notes,
            assumptions=list(WATER_BALANCE_ASSUMPTIONS),
            calculated_at=datetime.now(timezone.utc),
            **asdict(result),
        )

    def _get_organization(
        self,
        organization_id: int,
    ) -> Organization:
        organization = self.organization_repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found.",
            )

        return organization

    def _get_plant(
        self,
        plant_id: int,
    ) -> Plant:
        plant = self.plant_repository.get_by_id(plant_id)

        if plant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plant not found.",
            )

        return plant

    def _get_zone(
        self,
        zone_id: int,
    ) -> WaterAccountingZone:
        zone = self.zone_repository.get_by_id(zone_id)

        if zone is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Water Accounting Zone not found.",
            )

        return zone

    def _ensure_plant_ownership(
        self,
        plant: Plant,
        organization_id: int,
    ) -> None:
        if plant.organization_id != organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Plant does not belong to the specified "
                    "organization."
                ),
            )

    def _ensure_zone_ownership(
        self,
        zone: WaterAccountingZone,
        organization_id: int,
        plant_id: int,
    ) -> None:
        if (
            zone.organization_id != organization_id
            or zone.plant_id != plant_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Water Accounting Zone does not belong to the "
                    "specified Organization and Plant."
                ),
            )

    def _ensure_active(
        self,
        organization: Organization,
        plant: Plant,
        zone: WaterAccountingZone,
    ) -> None:
        if not organization.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organization is inactive.",
            )

        if not plant.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Plant is inactive.",
            )

        if not zone.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Water Accounting Zone is inactive.",
            )