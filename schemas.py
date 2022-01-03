"""
Pydantic models stored here
"""

from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base schema for User
    Attribute:
        - email: str
    """

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
        - username: str
        - ts_joined: datetime
    """

    user_id: int
    username: str
    ts_joined: datetime

    class Config:
        orm_mode = True


class UserHashed(UserBase):
    """
    Password schema
    Attributes:
        - password_hash: str

    """

    password_hash: str


class Video(BaseModel):
    """
    schema for video
    Attributes:
        - video_id: int
        - video_user_id: int
        - video_comment_id: int
        - video_name: str
        - original_video_quality: str
        - file_format: str
        - ts_upload: datetime
        - categories: Optional[str] = None
        - description: Optional[str] = None
        - length: int
        - no_likes: int
        - no_dislikes: int
    """

    video_id: int
    video_user_id: int
    video_comment_id: int
    video_name: str
    original_video_quality: str
    file_format: str
    ts_upload: datetime
    categories: Optional[str] = None
    description: Optional[str] = None
    length: int
    no_likes: int
    no_dislikes: int


class Comment(BaseModel):
    """
    Comment schema
    Attribute:
        - comment_id: int
        - comment_user_id: int
        - comment_content: str
        - ts_comment:  datetime
    """

    comment_id: int
    comment_user_id: int
    comment_content: str
    ts_comment: datetime
