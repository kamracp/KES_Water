from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.water_accounting_zone import WaterAccountingZone
from app.schemas.water_accounting_zone import (
    WaterAccountingZoneCreate,
    WaterAccountingZoneUpdate,
)


class WaterAccountingZoneRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        organization_id: int | None = None,
        plant_id: int | None = None,
    ) -> list[WaterAccountingZone]:
        statement = select(WaterAccountingZone)

        if organization_id is not None:
            statement = statement.where(
                WaterAccountingZone.organization_id == organization_id
            )

        if plant_id is not None:
            statement = statement.where(
                WaterAccountingZone.plant_id == plant_id
            )

        statement = statement.order_by(
            WaterAccountingZone.zone_name.asc()
        )

        return list(self.db.scalars(statement).unique().all())

    def get_by_id(
        self,
        zone_id: int,
    ) -> WaterAccountingZone | None:
        return self.db.get(WaterAccountingZone, zone_id)

    def get_by_code(
        self,
        organization_id: int,
        plant_id: int,
        zone_code: str,
    ) -> WaterAccountingZone | None:
        statement = select(WaterAccountingZone).where(
            WaterAccountingZone.organization_id == organization_id,
            WaterAccountingZone.plant_id == plant_id,
            WaterAccountingZone.zone_code == zone_code,
        )

        return self.db.scalar(statement)

    def create(
        self,
        payload: WaterAccountingZoneCreate,
    ) -> WaterAccountingZone:
        zone = WaterAccountingZone(**payload.model_dump())

        try:
            self.db.add(zone)
            self.db.commit()
            self.db.refresh(zone)
            return zone
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update(
        self,
        zone: WaterAccountingZone,
        payload: WaterAccountingZoneUpdate,
    ) -> WaterAccountingZone:
        update_data = payload.model_dump(exclude_unset=True)

        for field_name, field_value in update_data.items():
            setattr(zone, field_name, field_value)

        try:
            self.db.add(zone)
            self.db.commit()
            self.db.refresh(zone)
            return zone
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(
        self,
        zone: WaterAccountingZone,
    ) -> None:
        try:
            self.db.delete(zone)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise