from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.water_accounting_zone import (
    WaterAccountingZoneCreate,
    WaterAccountingZoneResponse,
    WaterAccountingZoneUpdate,
)
from app.services.water_accounting_zone_service import (
    WaterAccountingZoneService,
)


router = APIRouter(
    prefix="/water-accounting-zones",
    tags=["Water Accounting Zones"],
)


@router.get(
    "/",
    response_model=list[WaterAccountingZoneResponse],
    summary="List Water Accounting Zones",
)
def list_water_accounting_zones(
    organization_id: int | None = Query(
        default=None,
        gt=0,
    ),
    plant_id: int | None = Query(
        default=None,
        gt=0,
    ),
    db: Session = Depends(get_db),
) -> list[WaterAccountingZoneResponse]:
    service = WaterAccountingZoneService(db)
    return service.get_all(
        organization_id=organization_id,
        plant_id=plant_id,
    )


@router.get(
    "/{zone_id}",
    response_model=WaterAccountingZoneResponse,
    summary="Get Water Accounting Zone",
)
def get_water_accounting_zone(
    zone_id: int,
    db: Session = Depends(get_db),
) -> WaterAccountingZoneResponse:
    service = WaterAccountingZoneService(db)
    return service.get_by_id(zone_id)


@router.post(
    "/",
    response_model=WaterAccountingZoneResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Water Accounting Zone",
)
def create_water_accounting_zone(
    payload: WaterAccountingZoneCreate,
    db: Session = Depends(get_db),
) -> WaterAccountingZoneResponse:
    service = WaterAccountingZoneService(db)
    return service.create(payload)


@router.put(
    "/{zone_id}",
    response_model=WaterAccountingZoneResponse,
    summary="Update Water Accounting Zone",
)
def update_water_accounting_zone(
    zone_id: int,
    payload: WaterAccountingZoneUpdate,
    db: Session = Depends(get_db),
) -> WaterAccountingZoneResponse:
    service = WaterAccountingZoneService(db)
    return service.update(zone_id, payload)


@router.delete(
    "/{zone_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Water Accounting Zone",
)
def delete_water_accounting_zone(
    zone_id: int,
    db: Session = Depends(get_db),
) -> Response:
    service = WaterAccountingZoneService(db)
    service.delete(zone_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)