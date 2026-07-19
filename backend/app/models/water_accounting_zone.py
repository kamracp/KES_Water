
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.plant import Plant


class WaterAccountingZone(Base):
    __tablename__ = "water_accounting_zones"

    __table_args__ = (
        UniqueConstraint(
            "plant_id",
            "zone_code",
            name="uq_water_accounting_zones_plant_code",
        ),
        CheckConstraint(
            "metering_coverage_percent >= 0 "
            "AND metering_coverage_percent <= 100",
            name="ck_waz_metering_coverage_range",
        ),
        CheckConstraint(
            "audit_tolerance_percent >= 0 "
            "AND audit_tolerance_percent <= 100",
            name="ck_waz_audit_tolerance_range",
        ),
        CheckConstraint(
            "design_water_demand_m3_day IS NULL "
            "OR design_water_demand_m3_day >= 0",
            name="ck_waz_design_demand_nonnegative",
        ),
        CheckConstraint(
            "baseline_consumption_m3 IS NULL "
            "OR baseline_consumption_m3 >= 0",
            name="ck_waz_baseline_consumption_nonnegative",
        ),
        CheckConstraint(
            "baseline_end_date IS NULL "
            "OR baseline_start_date IS NULL "
            "OR baseline_end_date >= baseline_start_date",
            name="ck_waz_baseline_date_order",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    plant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "plants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    parent_zone_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "water_accounting_zones.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    zone_code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    zone_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    zone_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    audit_boundary_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    process_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    elevation_m: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 3),
        nullable=True,
    )

    design_water_demand_m3_day: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 3),
        nullable=True,
    )

    baseline_start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    baseline_end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    baseline_consumption_m3: Mapped[Decimal | None] = mapped_column(
        Numeric(16, 3),
        nullable=True,
    )

    water_balance_frequency: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="MONTHLY",
        server_default="MONTHLY",
    )

    metering_coverage_percent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0.00",
    )

    audit_tolerance_percent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("5.00"),
        server_default="5.00",
    )

    responsible_person: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    cost_center: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    is_audit_boundary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        index=True,
    )

    is_hydraulic_zone: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    organization: Mapped["Organization"] = relationship(
        lazy="joined",
    )

    plant: Mapped["Plant"] = relationship(
        lazy="joined",
    )

    parent_zone: Mapped["WaterAccountingZone | None"] = relationship(
        remote_side="WaterAccountingZone.id",
        back_populates="child_zones",
    )

    child_zones: Mapped[list["WaterAccountingZone"]] = relationship(
        back_populates="parent_zone",
    )

    def __repr__(self) -> str:
        return (
            f"<WaterAccountingZone(id={self.id}, "
            f"plant_id={self.plant_id}, "
            f"code='{self.zone_code}', "
            f"name='{self.zone_name}')>"
        )
