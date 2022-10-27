from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.schemas import PUserCreate
from api.core import security
from db.models import User


def get_user_by_login(active_session: Session, name: Optional[str]) -> User:
    return active_session.query(User).filter(User.login == name).first()


def get_user_by_id(active_session: Session, id_: int) -> User:
    return active_session.query(User).filter(User.id == id_).first()


def create(active_session: Session, user: PUserCreate) -> Optional[User]:
    unhashed_pwd = user.pwdhash
    if unhashed_pwd is None:
        return None
    hashed_pass = security.get_password_hash(unhashed_pwd)
    user.pwdhash = hashed_pass
    new_user = User(**user.dict())
    active_session.add(new_user)
    active_session.commit()
    active_session.refresh(new_user)
    return new_user
