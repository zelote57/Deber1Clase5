import jwt

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.config import ALGORITHM, SECRET_KEY
from db.database import SessionDep
from models.user import User
from services.auth_service import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
):
    authentication_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la autenticación",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise authentication_error
    except jwt.InvalidTokenError:
        raise authentication_error

    user = get_user_by_username(username, session)

    if user is None:
        raise authentication_error

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]