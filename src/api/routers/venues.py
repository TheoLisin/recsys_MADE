from api import schemas
from api.constants import RESPONSE_OK

from db.models import Venue
from db.db_params import get_session

from typing import List
from fastapi import HTTPException, APIRouter

from http import HTTPStatus

router = APIRouter(
    prefix="/venues",
    tags=["Venues"],
)


@router.get("/", response_model=List[schemas.PVenue])
def venues_get():
    with get_session() as session:
        return session.query(Venue).all()


@router.post("/", response_model=schemas.PVenue)
def venues_post(venue: schemas.PVenueCreate):
    """Adding new venue."""
    new_venue = Venue(**venue.dict())
    with get_session() as session:
        session.add(new_venue)
        session.commit()
        session.refresh(new_venue)
    return schemas.PVenue.from_orm(new_venue)


@router.get("/{id}", response_model=schemas.PVenue)
def venues_get_id(id: int):
    """Get venue by id."""
    with get_session() as session:
        venue = session.query(Venue).filter(Venue.id == id).first()
        if venue is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Venue with the given ID was not found"
            )
        return schemas.PVenue.from_orm(venue)


@router.put("/{id}", tags=["Venues"])
def venues_put_id(id: int, venue: schemas.PVenueCreate):
    """Update venue by id."""
    with get_session() as session:
        venue = session.query(Venue).filter(Venue.id == id).first()
        if venue is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Venue with the given ID was not found"
            )
    return RESPONSE_OK


@router.delete("/{id}", tags=["Venues"])
def venues_delete_id(id: int):
    """Update venue by id."""
    with get_session() as session:
        venue = session.query(Venue).filter(Venue.id == id).first()
        if venue is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Venue with the given ID was not found"
            )
        session.delete(venue)
        session.commit()
    return RESPONSE_OK