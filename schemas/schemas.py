"""
Pydantic models stored here
"""
# pylint: disable=import-error
# pylint: disable=too-few-public-methods

from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base schema for User
    Attribute:
        - username: str
        - email: str
    """

    username: str
    email: str


class UserCreate(UserBase):
    """
    UserCreate password
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
        - video_id: int
        - video_user_id: int
        - video_link: str
        - video_name: str
        - original_video_quality: str
        - file_format: str
        - ts_upload: datetime
        - categories: Optional[str] = None
        - description: Optional[str] = None
        - length: int
        - views: int
        - no_likes: int
        - no_dislikes: int
    """

    video_id: int
    video_user_id: int
    video_link: str
    video_name: str
    original_video_quality: str
    file_format: str
    ts_upload: datetime
    categories: Optional[str] = None
    description: Optional[str] = None
    length: int
    view: int
    no_likes: int
    no_dislikes: int


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
