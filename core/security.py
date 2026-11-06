from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict):
    content = data.copy()
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    content.update({"exp": expiration})

    return jwt.encode(content, SECRET_KEY, algorithm=ALGORITHM)