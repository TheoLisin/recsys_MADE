from api import schemas
from api.constants import RESPONSE_OK

from db.models import Reference
from db.db_params import get_session

from typing import List
from fastapi import HTTPException, APIRouter

from http import HTTPStatus

router = APIRouter(
    prefix="/references",
    tags=["References"],
)


@router.get("/", response_model=List[schemas.PReference])
def references_get():
    with get_session() as session:
        return session.query(Reference).all()


@router.post("/", response_model=schemas.PReference)
def references_post(reference: schemas.PReference):
    """Adding new reference."""
    new_reference = Reference(**reference.dict())
    with get_session() as session:
        session.add(new_reference)
        session.commit()
        session.refresh(new_reference)
    return schemas.PReference.from_orm(new_reference)


@router.get(
    "/{id_where}", response_model=schemas.PReference
)
def references_get_id(id_where: int):
    """Get reference by id_where."""
    with get_session() as session:
        reference = (
            session.query(Reference).filter(Reference.id_where == id_where).first()
        )
        if reference is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Reference with the given id_where was not found",
            )
        return schemas.PReference.from_orm(reference)


@router.delete("/", tags=["References"])
def references_delete_id(reference: schemas.PReference):
    """Update reference by id_where."""
    with get_session() as session:
        reference = (
            session.query(Reference)
            .filter(
                Reference.id_where == reference.id_where
                and Reference.id_what == reference.id_what
            )
            .first()
        )
        if reference is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Reference with the given id_where was not found",
            )
        session.delete(reference)
        session.commit()
    return RESPONSE_OK