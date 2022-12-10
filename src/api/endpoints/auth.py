from typing import Any
from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus

from api.schemas import PUser, PUserCreate
from api.crud import crud_user
from api.core.auth import access_token_response, authenticate
from api.deps import get_current_user
from api.core import api_config
from api.schemas import PUserInfo
from db.models import User
from db.db_params import get_session


router = APIRouter(tags=["Auth"])


@router.post("/signup", response_model=PUser, status_code=201)
def create_user_signup(*, user_in: PUserCreate):
    """Create new user without the need to be logged in."""
    with get_session() as active_session:
        user = crud_user.get_user_by_login(active_session, user_in.login)
        if user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="The user with this name already exists in the system",
            )

        new_user = crud_user.create(active_session, user_in)
        if new_user is None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Passoword need to be set.",
            )
        return PUser.from_orm(new_user)


@router.post(f"{api_config.API_V1_STR}/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """Get the JWT for a user with data from OAuth2 request form body."""
    with get_session() as active_session:
        user = authenticate(
            login=form_data.username,
            password=form_data.password,
            active_session=active_session,
        )
        if not user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Incorrect username or password",
            )

    return access_token_response(sub=user.id)


@router.get("/me", response_model=PUserInfo)
def my_articles(user: User = Depends(get_current_user)):
    # with get_session() as session:
    if user.author:
        return {
            "user": user,
            "author": user.author,
            "articles": user.author.articles,
        }

    return {"user": user, "author": None, "articles": None}
