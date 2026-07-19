from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.repositories.organization_repository import OrganizationRepository
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


class OrganizationService:
    def __init__(self, db: Session):
        self.repository = OrganizationRepository(db)

    def get_all(self) -> list[Organization]:
        return self.repository.get_all()

    def get_by_id(self, organization_id: int) -> Organization:
        organization = self.repository.get_by_id(organization_id)

        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found.",
            )

        return organization

    def create(self, payload: OrganizationCreate) -> Organization:
        existing = self.repository.get_by_code(payload.organization_code)

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Organization code "
                    f"'{payload.organization_code}' already exists."
                ),
            )

        return self.repository.create(payload)

    def update(
        self,
        organization_id: int,
        payload: OrganizationUpdate,
    ) -> Organization:
        organization = self.get_by_id(organization_id)

        if (
            payload.organization_code is not None
            and payload.organization_code != organization.organization_code
        ):
            existing = self.repository.get_by_code(
                payload.organization_code
            )

            if existing is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"Organization code "
                        f"'{payload.organization_code}' already exists."
                    ),
                )

        return self.repository.update(organization, payload)

    def delete(self, organization_id: int) -> None:
        organization = self.get_by_id(organization_id)
        self.repository.delete(organization)
