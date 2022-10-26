from api import schemas

from db.models import User
from db.db_params import get_session

from typing import List
from fastapi import HTTPException, APIRouter


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=List[schemas.PUser])
def users_get():
    with get_session() as session:
        return session.query(User).all()


@router.post("/", response_model=schemas.PUser)
def users_post(user: schemas.PUserCreate):
    """Adding new user."""
    new_user = User(**user.dict())
    with get_session() as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return schemas.PUser.from_orm(new_user)


@router.get("/{id}", response_model=schemas.PUser)
def users_get_id(id: int):
    """Get user by id."""
    with get_session() as session:
        user = session.query(User).filter(User.id == id).first()
        if user is None:
            raise HTTPException(
                status_code=404, detail="User with the given ID was not found"
            )
        return schemas.PUser.from_orm(user)


@router.put("/{id}")
def users_put_id(id: int, user: schemas.PUserCreate):
    """Update user by id."""
    with get_session() as session:
        user = session.query(User).filter(User.id == id).first()
        if user is None:
            raise HTTPException(
                status_code=404, detail="User with the given ID was not found"
            )
    return {"status": "OK"}


@router.delete("/{id}")
def users_delete_id(id: int):
    """Update user by id."""
    with get_session() as session:
        user = session.query(User).filter(User.id == id).first()
        if user is None:
            raise HTTPException(
                status_code=404, detail="User with the given ID was not found"
            )
        session.delete(user)
        session.commit()
    return {"status": "OK"}
