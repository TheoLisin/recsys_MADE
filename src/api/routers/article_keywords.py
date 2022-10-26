from api import schemas
from api.constants import RESPONSE_OK

from db.models import ArticleKeyword
from db.db_params import get_session

from typing import List
from fastapi import HTTPException, APIRouter

from http import HTTPStatus

router = APIRouter(
    prefix="/articlekeywords",
    tags=["ArticleKeywords"],
)


@router.get(
    "/",
    response_model=List[schemas.PArticleKeyword],
)
def articlekeywords_get():
    with get_session() as session:
        return session.query(ArticleKeyword).all()


@router.post(
    "/",
    response_model=schemas.PArticleKeyword,
)
def articlekeywords_post(articlekeyword: schemas.PArticleKeyword):
    """Adding new articlekeyword."""
    new_articlekeyword = ArticleKeyword(**articlekeyword.dict())
    with get_session() as session:
        session.add(new_articlekeyword)
        session.commit()
        session.refresh(new_articlekeyword)
    return schemas.PArticleKeyword.from_orm(new_articlekeyword)


@router.get(
    "/{id_article}",
    response_model=schemas.PArticleKeyword,
)
def articlekeywords_get_id(id_article: int):
    """Get articlekeyword by id_article."""
    with get_session() as session:
        articlekeyword = (
            session.query(ArticleKeyword)
            .filter(ArticleKeyword.id_article == id_article)
            .first()
        )
        if articlekeyword is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="ArticleKeyword with the given id_article was not found",
            )
        return schemas.PArticleKeyword.from_orm(articlekeyword)


@router.delete("/{id_article}", tags=["ArticleKeywords"])
def articlekeywords_delete_id(articlekeyword: schemas.PArticleKeyword):
    """Update articlekeyword by id_article."""
    with get_session() as session:
        articlekeyword = (
            session.query(ArticleKeyword)
            .filter(
                ArticleKeyword.id_article == articlekeyword.id_article
                and ArticleKeyword.id_keyword == articlekeyword.id_keyword
            )
            .first()
        )
        if articlekeyword is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="ArticleKeyword with the given id_article was not found",
            )
        session.delete(articlekeyword)
        session.commit()
    return RESPONSE_OK
