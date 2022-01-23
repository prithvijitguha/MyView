"""
Pydantic models stored here
"""
# pylint: disable=import-error
# pylint: disable=too-few-public-methods
# pylint: disable=no-name-in-module

from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base schema for User
    Attribute:
        - username: str
        - email: str
        - profile_picture: bool
    """

    username: str
    email: str
    profile_picture: bool


class UserCreate(UserBase):
    """
    UserCreate password.
    Inherits from UserBase
    Attributes:
        -password: str
    """

    password: str


class User(UserCreate):
    """
    User schema
    Attributes:
        - user_id: int
        - ts_joined: datetime
    """

    user_id: int
    ts_joined: datetime

    class Config:
        """
        Attributes can be accessed
        by both Schema.attribute
        or Schema["attribute"]
        """

        orm_mode = True


class Video(BaseModel):
    """
    schema for video
    Attributes:
        - video_user_id: int
        - video_link: str
        - video_name: str
        - video_height: int
        - video_width: int
        - file_format: str
        - ts_upload: datetime
        - categories: Optional[str] = None
        - description: Optional[str] = None
        - length: int
        - views: int
        - no_likes: int
        - no_dislikes: int
    """

    video_username: str
    video_link: str
    video_name: str
    video_height: int
    video_width: int
    file_format: str
    categories: Optional[str] = None
    description: Optional[str] = None
    length: int
    views: Optional[int] = 0
    no_likes: Optional[int] = 0
    no_dislikes: Optional[int] = 0


class Comment(BaseModel):
    """
    Comment schema
    Attribute:
        - comment_id: int
        - comment_user_id: int
        - comment_video_id
        - comment_content: str
        - ts_comment:  datetime
    """

    comment_id: List[int] = []
    comment_user_id: int
    comment_video_id: int
    comment_content: str
    ts_comment: datetime


class Token(BaseModel):
    """
    Token class
    Attributes:
        - email: str
    """

    email: str
