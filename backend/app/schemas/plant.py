
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PlantBase(BaseModel):
    organization_id: int = Field(gt=0)

    plant_code: str = Field(
        min_length=2,
        max_length=30,
    )
    plant_name: str = Field(
        min_length=2,
        max_length=150,
    )
    plant_type: str | None = Field(
        default=None,
        max_length=100,
    )

    address_line_1: str | None = Field(
        default=None,
        max_length=255,
    )
    address_line_2: str | None = Field(
        default=None,
        max_length=255,
    )

    country: str = Field(
        default="India",
        min_length=2,
        max_length=100,
    )
    state: str | None = Field(
        default=None,
        max_length=100,
    )
    city: str | None = Field(
        default=None,
        max_length=100,
    )
    postal_code: str | None = Field(
        default=None,
        max_length=20,
    )

    timezone: str = Field(
        default="Asia/Kolkata",
        min_length=2,
        max_length=50,
    )
    is_active: bool = True

    @field_validator("plant_code")
    @classmethod
    def normalize_plant_code(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator(
        "plant_name",
        "plant_type",
        "address_line_1",
        "address_line_2",
        "country",
        "state",
        "city",
        "postal_code",
        "timezone",
    )
    @classmethod
    def strip_text_values(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        return cleaned_value or None


class PlantCreate(PlantBase):
    pass


class PlantUpdate(BaseModel):
    organization_id: int | None = Field(
        default=None,
        gt=0,
    )

    plant_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
    )
    plant_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    plant_type: str | None = Field(
        default=None,
        max_length=100,
    )

    address_line_1: str | None = Field(
        default=None,
        max_length=255,
    )
    address_line_2: str | None = Field(
        default=None,
        max_length=255,
    )

    country: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    state: str | None = Field(
        default=None,
        max_length=100,
    )
    city: str | None = Field(
        default=None,
        max_length=100,
    )
    postal_code: str | None = Field(
        default=None,
        max_length=20,
    )

    timezone: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )
    is_active: bool | None = None

    @field_validator("plant_code")
    @classmethod
    def normalize_plant_code(
        cls,
        value: str | None,
    ) -> str | None:
        return value.strip().upper() if value is not None else None

    @field_validator(
        "plant_name",
        "plant_type",
        "address_line_1",
        "address_line_2",
        "country",
        "state",
        "city",
        "postal_code",
        "timezone",
    )
    @classmethod
    def strip_text_values(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        return cleaned_value or None


class PlantResponse(PlantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
