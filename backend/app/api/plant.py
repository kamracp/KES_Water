
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.plant import (
    PlantCreate,
    PlantResponse,
    PlantUpdate,
)
from app.services.plant_service import PlantService


router = APIRouter(
    prefix="/plants",
    tags=["Plants"],
)


@router.get(
    "/",
    response_model=list[PlantResponse],
    summary="List plants",
)
def list_plants(
    organization_id: int | None = Query(
        default=None,
        gt=0,
    ),
    db: Session = Depends(get_db),
) -> list[PlantResponse]:
    service = PlantService(db)
    return service.get_all(organization_id)


@router.get(
    "/{plant_id}",
    response_model=PlantResponse,
    summary="Get plant",
)
def get_plant(
    plant_id: int,
    db: Session = Depends(get_db),
) -> PlantResponse:
    service = PlantService(db)
    return service.get_by_id(plant_id)


@router.post(
    "/",
    response_model=PlantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create plant",
)
def create_plant(
    payload: PlantCreate,
    db: Session = Depends(get_db),
) -> PlantResponse:
    service = PlantService(db)
    return service.create(payload)


@router.put(
    "/{plant_id}",
    response_model=PlantResponse,
    summary="Update plant",
)
def update_plant(
    plant_id: int,
    payload: PlantUpdate,
    db: Session = Depends(get_db),
) -> PlantResponse:
    service = PlantService(db)
    return service.update(plant_id, payload)


@router.delete(
    "/{plant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete plant",
)
def delete_plant(
    plant_id: int,
    db: Session = Depends(get_db),
) -> Response:
    service = PlantService(db)
    service.delete(plant_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
