from api import schemas
from api.constants import RESPONSE_OK
from api.crud.crud_article import (
    YearFilter,
    AuthorNameFilter,
    VenueFilter,
    TagFilter,
    get_filtered_article,
)
from api.crud.crud_base import BaseFilter

from db.models import Article
from db.db_params import get_session

from typing import List, Optional
from fastapi import HTTPException, APIRouter

from http import HTTPStatus


router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)


@router.get("/", response_model=List[schemas.PArticle])
def articles_get():
    with get_session() as session:
        return session.query(Article).all()


@router.post("/", response_model=schemas.PArticle)
def articles_post(article: schemas.PArticleCreate):
    """Adding new article."""
    new_article = Article(**article.dict())
    with get_session() as session:
        session.add(new_article)
        session.commit()
        session.refresh(new_article)
    return schemas.PArticle.from_orm(new_article)


@router.get("/{id}", response_model=schemas.PArticle)
def articles_get_id(id: int):
    """Get article by id."""
    with get_session() as session:
        article = session.query(Article).filter(Article.id == id).first()
        if article is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Article with the given ID was not found",
            )
        return schemas.PArticle.from_orm(article)


@router.put("/{id}")
def articles_put_id(id: int, article: schemas.PArticleCreate):
    """Update article by id."""
    with get_session() as session:
        article = session.query(Article).filter(Article.id == id).first()
        if article is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Article with the given ID was not found",
            )
    return RESPONSE_OK


@router.delete("/{id}")
def articles_delete_id(id: int):
    """Update article by id."""
    with get_session() as session:
        article = session.query(Article).filter(Article.id == id).first()
        if article is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Article with the given ID was not found",
            )
        session.delete(article)
        session.commit()
    return RESPONSE_OK


@router.get("/search/{page}", response_model=List[schemas.PArticle])
def filter_article_by_year_author_journal(
    page: int,
    year: Optional[int] = None,
    author_name: Optional[str] = None,
    journal_name: Optional[str] = None,
    tag: Optional[str] = None,
):
    filters: List[BaseFilter] = []
    if year:
        filters.append(YearFilter(year))

    if author_name:
        filters.append(AuthorNameFilter(author_name))

    if journal_name:
        filters.append(VenueFilter(journal_name))

    if tag:
        filters.append(TagFilter(tag))

    if not filters:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="At least one filter parameter must be specified.",
        )

    with get_session() as active_session:
        return get_filtered_article(active_session, filters, page)
