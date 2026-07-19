from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.plant import Plant
from app.models.water_accounting_zone import WaterAccountingZone
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.plant_repository import PlantRepository
from app.repositories.water_accounting_zone_repository import (
    WaterAccountingZoneRepository,
)
from app.schemas.water_accounting_zone import (
    WaterAccountingZoneCreate,
    WaterAccountingZoneUpdate,
)


class WaterAccountingZoneService:
    def __init__(self, db: Session):
        self.zone_repository = WaterAccountingZoneRepository(db)
        self.organization_repository = OrganizationRepository(db)
        self.plant_repository = PlantRepository(db)

    def get_all(
        self,
        organization_id: int | None = None,
        plant_id: int | None = None,
    ) -> list[WaterAccountingZone]:
        if organization_id is not None:
            self._ensure_organization_exists(organization_id)

        if plant_id is not None:
            plant = self._get_plant(plant_id)

            if organization_id is not None:
                self._ensure_plant_belongs_to_organization(
                    plant,
                    organization_id,
                )

        return self.zone_repository.get_all(
            organization_id=organization_id,
            plant_id=plant_id,
        )

    def get_by_id(
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

    def create(
        self,
        payload: WaterAccountingZoneCreate,
    ) -> WaterAccountingZone:
        self._ensure_organization_exists(payload.organization_id)

        plant = self._get_plant(payload.plant_id)
        self._ensure_plant_belongs_to_organization(
            plant,
            payload.organization_id,
        )

        parent_zone_id = getattr(payload, "parent_zone_id", None)

        self._ensure_valid_parent_zone(
            parent_zone_id=parent_zone_id,
            organization_id=payload.organization_id,
            plant_id=payload.plant_id,
        )

        existing_zone = self.zone_repository.get_by_code(
            payload.organization_id,
            payload.plant_id,
            payload.zone_code,
        )

        if existing_zone is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Water Accounting Zone code '{payload.zone_code}' "
                    "already exists for this plant."
                ),
            )

        return self.zone_repository.create(payload)

    def update(
        self,
        zone_id: int,
        payload: WaterAccountingZoneUpdate,
    ) -> WaterAccountingZone:
        zone = self.get_by_id(zone_id)

        target_organization_id = (
            payload.organization_id
            if payload.organization_id is not None
            else zone.organization_id
        )

        target_plant_id = (
            payload.plant_id
            if payload.plant_id is not None
            else zone.plant_id
        )

        target_zone_code = (
            payload.zone_code
            if payload.zone_code is not None
            else zone.zone_code
        )

        self._ensure_organization_exists(target_organization_id)

        plant = self._get_plant(target_plant_id)
        self._ensure_plant_belongs_to_organization(
            plant,
            target_organization_id,
        )

        if "parent_zone_id" in payload.model_fields_set:
            target_parent_zone_id = getattr(
                payload,
                "parent_zone_id",
                None,
            )
        else:
            target_parent_zone_id = getattr(
                zone,
                "parent_zone_id",
                None,
            )

        self._ensure_valid_parent_zone(
            parent_zone_id=target_parent_zone_id,
            organization_id=target_organization_id,
            plant_id=target_plant_id,
            current_zone_id=zone.id,
        )

        existing_zone = self.zone_repository.get_by_code(
            target_organization_id,
            target_plant_id,
            target_zone_code,
        )

        if (
            existing_zone is not None
            and existing_zone.id != zone.id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Water Accounting Zone code '{target_zone_code}' "
                    "already exists for this plant."
                ),
            )

        return self.zone_repository.update(zone, payload)

    def delete(
        self,
        zone_id: int,
    ) -> None:
        zone = self.get_by_id(zone_id)
        self.zone_repository.delete(zone)

    def _ensure_organization_exists(
        self,
        organization_id: int,
    ) -> None:
        organization = self.organization_repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found.",
            )

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

    def _ensure_plant_belongs_to_organization(
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

    def _ensure_valid_parent_zone(
        self,
        parent_zone_id: int | None,
        organization_id: int,
        plant_id: int,
        current_zone_id: int | None = None,
    ) -> None:
        if parent_zone_id is None:
            return

        if (
            current_zone_id is not None
            and parent_zone_id == current_zone_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A zone cannot be its own parent.",
            )

        parent_zone = self.zone_repository.get_by_id(parent_zone_id)

        if parent_zone is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent Water Accounting Zone not found.",
            )

        if (
            parent_zone.organization_id != organization_id
            or parent_zone.plant_id != plant_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Parent zone must belong to the same "
                    "organization and plant."
                ),
            )