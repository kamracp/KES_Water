
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.plant import Plant
from app.schemas.plant import PlantCreate, PlantUpdate


class PlantRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        organization_id: int | None = None,
    ) -> list[Plant]:
        statement = select(Plant)

        if organization_id is not None:
            statement = statement.where(
                Plant.organization_id == organization_id
            )

        statement = statement.order_by(
            Plant.plant_name.asc()
        )

        return list(self.db.scalars(statement).unique().all())

    def get_by_id(self, plant_id: int) -> Plant | None:
        return self.db.get(Plant, plant_id)

    def get_by_code(
        self,
        organization_id: int,
        plant_code: str,
    ) -> Plant | None:
        statement = select(Plant).where(
            Plant.organization_id == organization_id,
            Plant.plant_code == plant_code,
        )

        return self.db.scalar(statement)

    def create(self, payload: PlantCreate) -> Plant:
        plant = Plant(**payload.model_dump())

        try:
            self.db.add(plant)
            self.db.commit()
            self.db.refresh(plant)
            return plant
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update(
        self,
        plant: Plant,
        payload: PlantUpdate,
    ) -> Plant:
        update_data = payload.model_dump(exclude_unset=True)

        for field_name, field_value in update_data.items():
            setattr(plant, field_name, field_value)

        try:
            self.db.add(plant)
            self.db.commit()
            self.db.refresh(plant)
            return plant
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, plant: Plant) -> None:
        try:
            self.db.delete(plant)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise
