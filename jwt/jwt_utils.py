"""
Create JWT tokens

"""

# flake8: noqa:E501
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=raise-missing-from

import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from db.database import get_db
from models import models
from schemas import schemas


load_dotenv()
SECRET_KEY = os.environ.get("JWT_SECRET")
ALGORITHM = os.environ.get("JWT_ALGO")
ACCESS_TOKEN_EXPIRES = 30

# path to get tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

cookie_sec = APIKeyCookie(name="session", auto_error=False)


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """ "
    create JWt access token
    Args:
        - data: dict
        - expires_delta: Optional[timedelta] = None

    Returns:
        - encodeed_jwt: bytes

    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Optional[str] = Depends(cookie_sec), db: Session = Depends(get_db)
):
    """
    check JWT of current user
    Args:
        - token: str = Depends(cookie_sec)
        - db:Session=Depends(get_db)

    Returns:
        - user
    Raises:
         - credentials_exception: if cannot validate credentials
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.Token(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_user_optional(
    user: Optional[schemas.User] = Depends(get_current_user),
) -> Optional[schemas.User]:
    """
    get current optional, not strict
    Args:
        - user: Optional[schemas.User] = Depends(get_current_user)

    Returns:
        - Optional[schemas.User]
    """
    return user
