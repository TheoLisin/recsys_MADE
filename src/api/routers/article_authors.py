from api import schemas

from db.models import ArticleAuthor
from db.db_params import get_session

from typing import List
from fastapi import HTTPException, APIRouter


router = APIRouter(
    prefix="/articleauthors",
    tags=["ArticleAuthors"],
)


@router.get(
    "/",
    response_model=List[schemas.PArticleAuthor],
)
def articleauthors_get():
    with get_session() as session:
        return session.query(ArticleAuthor).all()


@router.post(
    "/",
    response_model=schemas.PArticleAuthor,
)
def articleauthors_post(articleauthor: schemas.PArticleAuthor):
    """Adding new articleauthor."""
    new_articleauthor = ArticleAuthor(**articleauthor.dict())
    with get_session() as session:
        session.add(new_articleauthor)
        session.commit()
        session.refresh(new_articleauthor)
    return schemas.PArticleAuthor.from_orm(new_articleauthor)


@router.get(
    "/{id_article}",
    response_model=schemas.PArticleAuthor,
)
def articleauthors_get_id(id_article: int):
    """Get articleauthor by id_article."""
    with get_session() as session:
        articleauthor = (
            session.query(ArticleAuthor)
            .filter(ArticleAuthor.id_article == id_article)
            .first()
        )
        if articleauthor is None:
            raise HTTPException(
                status_code=404,
                detail="ArticleAuthor with the given id_article was not found",
            )
        return schemas.PArticleAuthor.from_orm(articleauthor)


@router.delete("/{id_article}", tags=["ArticleAuthors"])
def articleauthors_delete_id(articleauthor: schemas.PArticleAuthor):
    """Update articleauthor by id_article."""
    with get_session() as session:
        articleauthor = (
            session.query(ArticleAuthor)
            .filter(
                ArticleAuthor.id_article == articleauthor.id_article
                and ArticleAuthor.id_author == articleauthor.id_author,
            )
            .first(),
        )
        if articleauthor is None:
            raise HTTPException(
                status_code=404,
                detail="ArticleAuthor with the given id_article was not found",
            )
        session.delete(articleauthor)
        session.commit()
    return {"status": "OK"}
