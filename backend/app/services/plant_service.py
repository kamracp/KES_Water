
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.plant import Plant
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.plant_repository import PlantRepository
from app.schemas.plant import PlantCreate, PlantUpdate


class PlantService:
    def __init__(self, db: Session):
        self.plant_repository = PlantRepository(db)
        self.organization_repository = OrganizationRepository(db)

    def get_all(
        self,
        organization_id: int | None = None,
    ) -> list[Plant]:
        if organization_id is not None:
            self._ensure_organization_exists(organization_id)

        return self.plant_repository.get_all(organization_id)

    def get_by_id(self, plant_id: int) -> Plant:
        plant = self.plant_repository.get_by_id(plant_id)

        if plant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plant not found.",
            )

        return plant

    def create(self, payload: PlantCreate) -> Plant:
        self._ensure_organization_exists(payload.organization_id)

        existing_plant = self.plant_repository.get_by_code(
            payload.organization_id,
            payload.plant_code,
        )

        if existing_plant is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Plant code '{payload.plant_code}' already exists "
                    "for this organization."
                ),
            )

        return self.plant_repository.create(payload)

    def update(
        self,
        plant_id: int,
        payload: PlantUpdate,
    ) -> Plant:
        plant = self.get_by_id(plant_id)

        target_organization_id = (
            payload.organization_id
            if payload.organization_id is not None
            else plant.organization_id
        )

        target_plant_code = (
            payload.plant_code
            if payload.plant_code is not None
            else plant.plant_code
        )

        if payload.organization_id is not None:
            self._ensure_organization_exists(
                payload.organization_id
            )

        existing_plant = self.plant_repository.get_by_code(
            target_organization_id,
            target_plant_code,
        )

        if (
            existing_plant is not None
            and existing_plant.id != plant.id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Plant code '{target_plant_code}' already exists "
                    "for this organization."
                ),
            )

        return self.plant_repository.update(plant, payload)

    def delete(self, plant_id: int) -> None:
        plant = self.get_by_id(plant_id)
        self.plant_repository.delete(plant)

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
