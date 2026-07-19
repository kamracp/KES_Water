
from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.services.organization_service import OrganizationService


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.get(
    "/",
    response_model=list[OrganizationResponse],
    summary="List organizations",
)
def list_organizations(
    db: Session = Depends(get_db),
) -> list[OrganizationResponse]:
    service = OrganizationService(db)
    return service.get_all()


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
    summary="Get organization",
)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    service = OrganizationService(db)
    return service.get_by_id(organization_id)


@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create organization",
)
def create_organization(
    payload: OrganizationCreate,
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    service = OrganizationService(db)
    return service.create(payload)


@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse,
    summary="Update organization",
)
def update_organization(
    organization_id: int,
    payload: OrganizationUpdate,
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    service = OrganizationService(db)
    return service.update(organization_id, payload)


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete organization",
)
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
) -> Response:
    service = OrganizationService(db)
    service.delete(organization_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
