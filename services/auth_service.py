from sqlmodel import Session, select

from core.security import hash_password, verify_password
from models.user import User
from schemas.user import UserCreate


def register_user(data: UserCreate, session: Session):
    existing_user = session.exec(
        select(User).where(
            (User.username == data.username) | (User.email == data.email)
        )
    ).first()

    if existing_user:
        return None

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def authenticate_user(username: str, password: str, session: Session):
    user = get_user_by_username(username, session)

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def get_user_by_username(username: str, session: Session):
    return session.exec(
        select(User).where(User.username == username)
    ).first()