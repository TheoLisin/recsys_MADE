from typing import Any, Dict, Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt


from db.models import User
from api.core import api_config
from api.core.security import verify_password
from api.crud.crud_user import get_user_by_login


JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{api_config.API_V1_STR}/auth/login")


def authenticate(
    *,
    login: str,
    password: str,
    active_session: Session,
) -> Optional[User]:
    user = get_user_by_login(active_session, login)
    if not user:
        return None
    if not verify_password(password, user.pwdhash):
        return None
    return user


def access_token_response(*, sub: str) -> Dict[str, str]:
    resp = {}
    token = _create_access_token(sub=sub)
    resp["access_token"] = token
    resp["token_type"] = "bearer"

    return resp


def _create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=api_config.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload: Dict[str, Any] = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, api_config.JWT_SECRET, algorithm=api_config.ALGORITHM)
