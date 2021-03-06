"""All sqlalchemy models"""

# pylint: disable=import-error
# pylint: disable=too-few-public-methods

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    """
    User model for each user
    Attributes:
        - user_id: int, non-nullable, unique
        - username: str, non-nullable, unique
        - email: str, non-nullable, unique
        - profile_picture: bool, nullable
        - ts_joined: datetime, non-nullable

    Relationships:
        - primary_key: user_id
    """

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    profile_picture = Column(Boolean, default=False)
    ts_joined = Column(DateTime)
    admin = Column(Boolean, default=False)

    uploaded = relationship("Video", back_populates="user")


class UserHashed(Base):
    """
    Usersecrets

    tablename: users_hashes
    Attributes:
        - user_email: string, foreign_key, non-nullable, unique
        - password_hash: string, non-nullable, unique
        - ts_created: datetime, non-nullable
    """

    __tablename__ = "users_hashes"
    user_email = Column(
        String, ForeignKey("users.email"), primary_key=True, unique=True
    )
    password_hash = Column(String)
    ts_created = Column(DateTime)


class Video(Base):
    """
    model for video_library.
    Contains all data for videos

    tablename: video_library
    Attributes:
        - video_id: int, non-nullable, primary_key
        - video_username: str, non-nullable, foreign_key
        - video_link: string, non-nullable, unique
        - video_name: string, non-nullable,
        - video_height: int, non-nullable,
        - video_width: int, non-nullable,
        - file_format: string, non-nullable,
        - ts_upload: datetime, non-nullable,
        - categories: string, nullable,
        - description: string, nullable,
        - length: int, non-nullable,
        - views: int, non-nullable
        - no_likes: int, non-nullable,
        - no_dislikes: int, non-nullable,

    """

    __tablename__ = "video_library"

    video_id = Column(Integer, primary_key=True, index=True)
    video_username = Column(String, ForeignKey("users.username"))
    video_link = Column(String, unique=True)
    video_name = Column(String)
    video_height = Column(Integer)
    video_width = Column(Integer)
    file_format = Column(String)
    ts_upload = Column(DateTime)
    categories = Column(String, nullable=True)
    description = Column(String, nullable=True)
    length = Column(Integer)
    views = Column(Integer)
    no_likes = Column(Integer)
    no_dislikes = Column(Integer)

    user = relationship("User", back_populates="uploaded")


class Comment(Base):
    """
    Comments on videos

    tablename: comments
    Attributes:
        - comment_id: int, primary, index
        - comment_user_id: int,
        - comment_video_id: int,
        - comment_content: string,
        - ts_comment: datetime,
    """

    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    comment_user_id = Column(Integer, ForeignKey("users.user_id"))
    comment_video_id = Column(Integer, ForeignKey("video_library.video_id"))
    comment_content = Column(Text)
    ts_comment = Column(DateTime)


class VideoViews(Base):
    """
    Tracks all user views
    tablename: video_views
    Attributes:
        - video_view_id
        - video_id
        - user_id
    """

    __tablename__ = "video_views"
    video_view_id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("video_library.video_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))


class UserLikesDislikes(Base):
    """ "
    Tracks all user likes

    Tablename: user_likes_dislikes

    Attributes:
        - like_id
        - like_user_id
        - like_video_id
        - like_dislike
    """

    __tablename__ = "user_likes_dislikes"

    like_id = Column(Integer, primary_key=True, index=True)
    like_user_id = Column(Integer, ForeignKey("users.user_id"))
    like_video_id = Column(Integer, ForeignKey("video_library.video_id"))
    like_dislike = Column(Boolean)
