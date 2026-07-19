from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class OrganizationBase(BaseModel):
    organization_code: str = Field(min_length=2, max_length=30)
    organization_name: str = Field(min_length=2, max_length=150)

    industry: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    website: str | None = Field(default=None, max_length=255)

    country: str = Field(default="India", min_length=2, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)

    timezone: str = Field(default="Asia/Kolkata", max_length=50)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    is_active: bool = True

    @field_validator("organization_code")
    @classmethod
    def normalize_organization_code(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator(
        "organization_name",
        "industry",
        "phone",
        "website",
        "country",
        "state",
        "city",
        "timezone",
    )
    @classmethod
    def strip_text_values(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        return cleaned_value or None

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.strip().upper()


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    organization_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
    )
    organization_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    industry: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    website: str | None = Field(default=None, max_length=255)

    country: str | None = Field(default=None, min_length=2, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)

    timezone: str | None = Field(default=None, max_length=50)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    is_active: bool | None = None

    @field_validator("organization_code")
    @classmethod
    def normalize_organization_code(cls, value: str | None) -> str | None:
        return value.strip().upper() if value is not None else None

    @field_validator(
        "organization_name",
        "industry",
        "phone",
        "website",
        "country",
        "state",
        "city",
        "timezone",
    )
    @classmethod
    def strip_text_values(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        return cleaned_value or None

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str | None) -> str | None:
        return value.strip().upper() if value is not None else None


class OrganizationResponse(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime