from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.security import create_access_token
from db.database import SessionDep
from schemas.user import Token, UserCreate, UserRead
from services.auth_service import authenticate_user, register_user

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(data: UserCreate, session: SessionDep):
    user = register_user(data, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o email ya existen.",
        )

    return user


@router.post("/login", response_model=Token)
def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    user = authenticate_user(data.username, data.password, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer",
    }