from api import schemas
from api.constants import RESPONSE_OK

from db.models import Article
from db.db_params import get_session

from typing import List
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
