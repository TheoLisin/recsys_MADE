from typing import List, Optional
from fastapi import HTTPException, APIRouter, Depends

from sqlalchemy import func
from http import HTTPStatus
from numpy.random import randint, seed

from api import schemas
from api.constants import RESPONSE_OK
from api.crud.crud_article import (
    YearFilter,
    AuthorNameFilter,
    VenueFilter,
    TagFilter,
    get_filtered_article,
    get_art_titile_tag,
    get_references,
)
from api.crud.crud_authors import get_author_articles

from api.crud.crud_base import BaseFilter
from api.conf_paths import MODELS_PATH
from api.deps import get_current_user
from api.core.api_config import PAGINATION_LIMIT

from db.models import Article, User, Author
from db.db_params import get_session
from ml.article_recommendation_lda.article_recommendation import ArticleRecommendation


router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)

# model_article_rec = ArticleRecommendation(MODELS_PATH)

@router.get("/", response_model=List[schemas.PArticle])
def articles_get(page: int):
    with get_session() as session:
        return (
            session.query(Article)
            .limit(PAGINATION_LIMIT)
            .offset((page - 1) * PAGINATION_LIMIT)
            .all()
        )


@router.post("/", response_model=schemas.PArticle)
def articles_post(article: schemas.PArticleCreate):
    """Adding new article."""
    new_article = Article(**article.dict())
    with get_session() as session:
        session.add(new_article)
        session.commit()
        session.refresh(new_article)
    return schemas.PArticle.from_orm(new_article)


@router.get("/search", response_model=List[schemas.PArticle])
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


@router.get("/recommend", response_model=List[schemas.PArticleRec])
def get_art_recommendation(page: int, user: User = Depends(get_current_user)):
    with get_session() as session:
        if user.author:
            auth_id = user.author.id
            arts = get_author_articles(session, auth_id)
            refs = get_references(session, arts)

            if (page < 0) or (page >= len(refs)):
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail="Page not found",
                )

            # rec_articles_np = model_article_rec.get_recommendations(refs[page])
        else:
            max_art = session.query(func.max(Article.id)).first()[0]
            seed(user.id + page)
            rec_articles_np = randint(1, max_art, size=10)

    rec_articles = [int(rec) for rec in rec_articles_np]
    return get_art_titile_tag(session, rec_articles)


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
