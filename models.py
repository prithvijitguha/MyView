"""All sqlalchemy models"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Text

from .database import Base


class User(Base):
    """
    User model for each user
    Attributes:
        - user_id: int, non-nullable, unique
        - username: str, non-nullable, unique
        - email: str, non-nullable, unique
        - ts_joined: datetime, non-nullable

    Relationships:
        - primary_key: user_id
    """

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    ts_joined = Column(DateTime)


class UserHashed(Base):
    """
    Usersecrets

    tablename: users_hashes
    Attributes:
        - user_email: int, foreign_key, non-nullable, unique
        - password_hash: string, non-nullable, unique
        - ts_created: datetime, non-nullable
    """

    __tablename__ = "users_hashes"
    user_email = Column(Integer, ForeignKey("users.email"), unique=True)
    password_hash = Column(String)
    ts_created = Column(DateTime)


class Video(Base):
    """
    model for video_library.
    Contains all data for videos

    tablename: video_library
    Attributes:
        - video_id: int, non-nullable, primary_key
        - video_user_id: int, non-nullable, foreign_key
        - comment_id: int, non-nullable,
        - video_name: string, non-nullable,
        - original_video_quality: string, non-nullable,
        - file_format: string, non-nullable,
        - ts_upload: datetime, non-nullable,
        - categories: string, nullable,
        - description: string, nullable,
        - length: int, non-nullable,
        - no_likes: int, non-nullable,
        - no_dislikes: int, non-nullable,

    """

    __tablename__ = "video_library"

    video_id = Column(Integer, primary_key=True, index=True)
    video_user_id = Column(Integer, ForeignKey("users.user_id"))
    video_comment_id = Column(Integer, ForeignKey("comments.comment_id"))
    video_name = Column(String)
    original_video_quality = Column(String)
    file_format = Column(String)
    ts_upload = Column(DateTime)
    categories = Column(String, nullable=True)
    description = Column(String, nullable=True)
    length = Column(Integer)
    no_likes = Column(Integer)
    no_dislikes = Column(Integer)


class Comment(Base):
    """
    Comments on videos

    tablename: comments
    Attributes:
        - comment_id: int, primary, index
        - user_id: int,
        - comment_content: string,
        - ts_comment: datetime,
    """

    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    comment_user_id = Column(Integer, ForeignKey("users.user_id"))
    comment_content = Column(Text)
    ts_comment = Column(DateTime)
