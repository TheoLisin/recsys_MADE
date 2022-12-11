from typing import List
from api import schemas
from api.constants import RESPONSE_OK
from api.deps import get_current_user
from api.crud.crud_authors import get_auth_recommendation
from api.crud.crud_base import get_random_subset
from api.core.api_config import PAGINATION_LIMIT

from db.models import Author, User
from db.db_params import get_session

from fastapi import HTTPException, APIRouter, Depends

from http import HTTPStatus

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.get("/", response_model=List[schemas.PAuthor])
def authors_get(page: int):
    with get_session() as session:
        return (
            session.query(Author)
            .limit(PAGINATION_LIMIT)
            .offset((page - 1) * PAGINATION_LIMIT)
            .all()
        )


@router.post("/", response_model=schemas.PAuthor)
def authors_post(author: schemas.PAuthorCreate):
    """Adding new author."""
    new_author = Author(**author.dict())
    with get_session() as session:
        session.add(new_author)
        session.commit()
        session.refresh(new_author)
    return schemas.PAuthor.from_orm(new_author)


@router.get("/recommend", response_model=List[schemas.PAuthorRec])
def get_coauth_recommendation(user: User = Depends(get_current_user)):

    if user.author is None:
        return []

    id_author = user.author.id

    with get_session() as session:
        recs = get_auth_recommendation(session, id_author=id_author)
        recs_subset = get_random_subset(recs, size=10)

        for pos, auth in enumerate(recs_subset):
            name = (
                session.query(Author.name)
                .filter(Author.id == auth["id_author"])
                .first()[0]
            )
            recs_subset[pos]["name"] = name

    return recs_subset


@router.get("/{id}", response_model=schemas.PAuthorInfo)
def authors_get_id(id: int):
    """Get author by id."""
    with get_session() as session:
        author: Author = session.query(Author).filter(Author.id == id).first()
        if author is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Author with the given ID was not found",
            )
    return {"id_author": author.id, "author": author, "articles": author.articles}


@router.put("/{id}", tags=["Authors"])
def authors_put_id(id: int, author: schemas.PAuthorCreate):
    """Update author by id."""
    with get_session() as session:
        author = session.query(Author).filter(Author.id == id).first()
        if author is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Author with the given ID was not found",
            )
    return RESPONSE_OK


@router.delete("/{id}", tags=["Authors"])
def authors_delete_id(id: int):
    """Update author by id."""
    with get_session() as session:
        author = session.query(Author).filter(Author.id == id).first()
        if author is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Author with the given ID was not found",
            )
        session.delete(author)
        session.commit()
    return RESPONSE_OK
