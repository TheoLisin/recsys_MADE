from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from api.core.auth import oauth2_scheme
from api.core import api_config
from api.crud.crud_user import get_user_by_id
from db.db_params import get_session
from db.models import User


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            api_config.JWT_SECRET,
            algorithms=[api_config.ALGORITHM],
            options={"verify_aud": False},
        )

        userid: str = payload.get("sub")

        if userid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with get_session() as active_session:
        user = get_user_by_id(active_session, userid)

    if user is None:
        raise credentials_exception

    return user
