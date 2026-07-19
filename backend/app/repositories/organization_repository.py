from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Organization]:
        statement = select(Organization).order_by(
            Organization.organization_name.asc()
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, organization_id: int) -> Organization | None:
        return self.db.get(Organization, organization_id)

    def get_by_code(self, organization_code: str) -> Organization | None:
        statement = select(Organization).where(
            Organization.organization_code == organization_code
        )
        return self.db.scalar(statement)

    def create(self, payload: OrganizationCreate) -> Organization:
        organization = Organization(**payload.model_dump())

        try:
            self.db.add(organization)
            self.db.commit()
            self.db.refresh(organization)
            return organization
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update(
        self,
        organization: Organization,
        payload: OrganizationUpdate,
    ) -> Organization:
        update_data = payload.model_dump(exclude_unset=True)

        for field_name, field_value in update_data.items():
            setattr(organization, field_name, field_value)

        try:
            self.db.add(organization)
            self.db.commit()
            self.db.refresh(organization)
            return organization
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, organization: Organization) -> None:
        try:
            self.db.delete(organization)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise
