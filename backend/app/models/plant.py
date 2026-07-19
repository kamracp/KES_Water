
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.organization import Organization


class Plant(Base):
    __tablename__ = "plants"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "plant_code",
            name="uq_plants_organization_code",
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

    plant_code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    plant_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    plant_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    address_line_1: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="India",
        server_default="India",
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    timezone: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Asia/Kolkata",
        server_default="Asia/Kolkata",
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

    def __repr__(self) -> str:
        return (
            f"<Plant(id={self.id}, "
            f"organization_id={self.organization_id}, "
            f"code='{self.plant_code}', "
            f"name='{self.plant_name}')>"
        )
