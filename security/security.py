"""
Module to create JWT
"""
# flake8: noqa:E501
# pylint: disable=import-error

import os
from typing import Optional
from datetime import datetime, timedelta

from jose import jwt


SECRET_KEY = os.environ.get("SECRET_KEY_JWT")
ALGORITHM = os.environ.get("JWT_ALGO")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRES"))


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create access token
    Args:
        data: dict
        expires_delta: Optional[timedelta] = None

    Returns:
        encoded_jwt
    """
    # create copy of data
    to_encode = data.copy()
    # if optional argument expirary given
    # set it to delta time from now
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    # otherwise set it to default
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # update the expirary
    to_encode.update({"exp": expire})
    # encode the token with secret key and algo
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # return the token
    return encoded_jwt
