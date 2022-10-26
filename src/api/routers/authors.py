from api import schemas
from api.constants import RESPONSE_OK

from db.models import Author
from db.db_params import get_session

from typing import List
from fastapi import HTTPException, APIRouter

from http import HTTPStatus

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.get("/", response_model=List[schemas.PAuthor])
def authors_get():
    with get_session() as session:
        return session.query(Author).all()


@router.post("/", response_model=schemas.PAuthor)
def authors_post(author: schemas.PAuthorCreate):
    """Adding new author."""
    new_author = Author(**author.dict())
    with get_session() as session:
        session.add(new_author)
        session.commit()
        session.refresh(new_author)
    return schemas.PAuthor.from_orm(new_author)


@router.get("/{id}", response_model=schemas.PAuthor)
def authors_get_id(id: int):
    """Get author by id."""
    with get_session() as session:
        author = session.query(Author).filter(Author.id == id).first()
        if author is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Author with the given ID was not found"
            )
    return schemas.PAuthor.from_orm(author)


@router.put("/{id}", tags=["Authors"])
def authors_put_id(id: int, author: schemas.PAuthorCreate):
    """Update author by id."""
    with get_session() as session:
        author = session.query(Author).filter(Author.id == id).first()
        if author is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Author with the given ID was not found"
            )
    return RESPONSE_OK


@router.delete("/{id}", tags=["Authors"])
def authors_delete_id(id: int):
    """Update author by id."""
    with get_session() as session:
        author = session.query(Author).filter(Author.id == id).first()
        if author is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Author with the given ID was not found"
            )
        session.delete(author)
        session.commit()
    return RESPONSE_OK
