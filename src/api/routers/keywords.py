# from api import schemas
# from api.constants import RESPONSE_OK

# from db.models import Keyword
# from db.db_params import get_session

# from typing import List
# from fastapi import HTTPException, APIRouter

# from http import HTTPStatus

# router = APIRouter(
#     prefix="/keywords",
#     tags=["Keywords"],
# )


# @router.get("/", response_model=List[schemas.PKeyword])
# def keywords_get():
#     with get_session() as session:
#         return session.query(Keyword).all()


# @router.post("/", response_model=schemas.PKeyword)
# def keywords_post(keyword: schemas.PKeywordCreate):
#     """Adding new keyword."""
#     new_keyword = Keyword(**keyword.dict())
#     with get_session() as session:
#         session.add(new_keyword)
#         session.commit()
#         session.refresh(new_keyword)
#     return schemas.PKeyword.from_orm(new_keyword)


# @router.get("/{id}", response_model=schemas.PKeyword)
# def keywords_get_id(id: int):
#     """Get keyword by id."""
#     with get_session() as session:
#         keyword = session.query(Keyword).filter(Keyword.id == id).first()
#         if keyword is None:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND, detail="Keyword with the given ID was not found"
#             )
#         return schemas.PKeyword.from_orm(keyword)


# @router.put("/{id}", tags=["Keywords"])
# def keywords_put_id(id: int, keyword: schemas.PKeywordCreate):
#     """Update keyword by id."""
#     with get_session() as session:
#         keyword = session.query(Keyword).filter(Keyword.id == id).first()
#         if keyword is None:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND, detail="Keyword with the given ID was not found"
#             )
#     return RESPONSE_OK


# @router.delete("/{id}", tags=["Keywords"])
# def keywords_delete_id(id: int):
#     """Update keyword by id."""
#     with get_session() as session:
#         keyword = session.query(Keyword).filter(Keyword.id == id).first()
#         if keyword is None:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND, detail="Keyword with the given ID was not found"
#             )
#         session.delete(keyword)
#         session.commit()
#     return RESPONSE_OK
