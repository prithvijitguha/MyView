"""
Reusable functions to interact with the database
CRUD: Create, Read, Update, and Delete.
"""

# flake8: noqa:E501, F821
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=broad-except
# pylint: disable=undefined-variable

from datetime import datetime, timezone
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models import models
from schemas import schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str):
    """
    Function to generate hash string for password
    Args:
        - plain_password: str
    Returns:
        - hashed_password: str

    Example:
    `
    >>> plain_password = "test"
    >>> hash_password(plain_password)
    hashed_password_string
    `
    """
    return pwd_context.hash(plain_password)


def compare_password(plain_password: str, hashed_password: str):
    """
    Function to compare password plain with hash.
    Returns True if password matches hash, False otherwise
    Args:
        - plain_password: str
        - hashed_password: str

    Returns:
        - Boolean

    Example:
    `
    >>> plain_password = "test"
    >>> hashed_password = "test_hashed_password"
    >>> compare_password(plain_password, hashed_password)
    True`
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    """
    Check if user is authenticated

    Args:
        - db: Session
        - username: str
        - password: str
    """
    # get current user
    # get user_id of current user
    user_id = (
        db.query(models.User).filter(models.User.username == username).first().user_id
    )
    user = get_user(db, user_id)
    if not user:
        return False
    # get the user email
    check_email = user.email
    # get the row from UserHash table
    db_UserHash = (
        db.query(models.UserHashed)
        .filter(models.UserHashed.user_email == check_email)
        .first()
    )
    # get the hash value
    hashed_password = db_UserHash.password_hash
    if not compare_password(password, hashed_password):
        return False
    return user


def authenticate_user_email(db: Session, email: str, password: str):
    """
    Check if user is authenticated
    by email
    """
    # get current user
    user = db.query(models.User).filter(models.User.email == email).first()
    # authenticate user
    if user and authenticate_user(db, user.username, password):
        return True
    return False


def get_timestamp_now():
    """Function to get current datetime stamp in utc timezone.
    Args:
        - None
    Returns:
        - datetime.object
    Example:
    `
    >>> get_timestamp_now()
    2022-01-04 08:17:18.990273+00:00
    `
    """
    return datetime.now(timezone.utc)


def create_user(db: Session, user: schemas.UserCreate):
    """
    Function to create user to `users` table and
    password to `users_hashes` table.
    Uses schemas.User to add to models.User
    models.User attributes:
        - user_id: int, non-nullable, unique
        - username: str, non-nullable, unique
        - email: str, non-nullable, unique
        - profile_picture: bool
        - ts_joined: datetime, non-nullable

    models.UserHashed attributes:
        - user_email: int, foreign_key, non-nullable, unique
        - password_hash: string, non-nullable, unique
        - ts_created: datetime, non-nullable

    Args:
        - db: Session
        - user: schemas.User
    Returns:
        - db_user Object
    """
    # hash the password
    hashed_password = hash_password(user.password)
    # generate timestamp
    timestamp = get_timestamp_now()
    # create model for User
    db_user = models.User(
        username=user.username,
        email=user.email,
        profile_picture=user.profile_picture,
        ts_joined=timestamp,
    )
    # create model for UserHashed
    db_user_hashed = models.UserHashed(
        user_email=user.email, password_hash=hashed_password, ts_created=timestamp
    )
    # add both model instances to database
    db.add(db_user)
    db.add(db_user_hashed)
    db.commit()
    db.refresh(db_user)
    db.refresh(db_user_hashed)
    return db_user


# def get user
def get_user(db: Session, user_id: int):
    """get user from table `users`
    by id
    Args:
        - db: Session object
        - user_id: int

    Returns:
        - db query instance
    """
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_username(db: Session, user_id: int):
    """get username from user_id"""
    return db.query(models.User).filter(models.User.user_id == user_id).first().username


def get_user_by_email(db: Session, email: str):
    """get user from table `users`
    by email
    Args:
        - db: Session
        - email: str
    Returns:
        - db query instance
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    """get user from table `users`
    by email
    Args:
        - db: Session
        - username: str
    Returns:
        - db query instance
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_id(db: Session, username: str):
    """get user id from username
    Args:
        - db: Session
        - username: str

    Returns:
        - user_int: int
    """
    user = db.query(models.User).filter(models.User.username == username).first()
    return user.user_id


# def delete user
def delete_user(db: Session, user_id: int):
    """Used to delete user from table `users`
    Args:
        - db: Session
        - user_id: int
    Returns:
        - Boolean
    """
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    try:
        db.delete(db_user)
        db.commit()
        db.refresh(db_user)
        return True
    except Exception as e:
        print(f"Could not delete user={user_id}: {e}")
        return False


# def add video to library
def add_video(db: Session, video: schemas.Video):
    """
    Adds video to table video_library
    model used is Video.
    Attributes:
        - video_user_id: int, non-nullable, foreign_key
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

    Args:
        - db: Session
        - video: schemas.Video
    Returns:
        - db_video object
    """
    db_video = models.Video(
        video_username=video.video_username,
        video_link=video.video_link,
        video_name=video.video_name,
        video_height=video.video_height,
        video_width=video.video_width,
        file_format=video.file_format,
        ts_upload=get_timestamp_now(),
        categories=video.categories,
        description=video.description,
        length=video.length,
        views=video.views,
        no_likes=video.no_likes,
        no_dislikes=video.no_dislikes,
    )
    # add to database
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


# increment view by one
def increase_view(db: Session, video_int: int, active_user: schemas.User):
    """
    Increases the value of view of a
    video by 1 int

    Args:
        - db
        - video_int

    Returns:
        - None
    """
    # get the video
    video = get_video(db, video_int)
    if active_user:
        user = (
            db.query(models.User)
            .filter(models.User.user_id == active_user.user_id)
            .first()
        )
        video_view = models.VideoViews(video_id=video.video_id, user_id=user.user_id)
        db.add(video_view)
        db.commit()
        db.refresh(video_view)
    # record unknown user views also
    else:
        video_view = models.VideoViews(video_id=video.video_id, user_id=None)
        db.add(video_view)
        db.commit()
        db.refresh(video_view)
    # incease by 1
    video.views += 1
    # commit to database
    db.add(video)
    db.commit()
    db.refresh(video)


def check_like_dislike(db: Session, video_id: str, user_id: int):
    """Check if user has liked or disliked
    the video before
    """
    like_model = (
        db.query(models.UserLikesDislikes)
        .filter(
            models.UserLikesDislikes.like_user_id == user_id,
            models.UserLikesDislikes.like_video_id == video_id,
        )
        .first()
    )
    return like_model


def video_like(db: Session, video_int: str, user_id: int):
    """Adds a like to video"""
    # query the database for video
    video = get_video(db, video_int)
    user = get_user(db, user_id)
    # check if user has like before
    # check if entry is dislike
    like_entry = check_like_dislike(db, video.video_id, user.user_id)
    # if user already liked before
    if like_entry and like_entry.like_dislike is True:
        return None
    # if user has disliked before
    if like_entry and like_entry.like_dislike is False:
        like_entry.like_dislike = True
        # reduce dislikes by 1
        video.no_dislikes -= 1
        db.add(like_entry)
        db.commit()
        db.refresh(like_entry)
    # if not liked before
    else:
        like_model = models.UserLikesDislikes(
            like_user_id=user.user_id, like_video_id=video.video_id, like_dislike=True
        )
        db.add(like_model)
        db.commit()
        db.refresh(like_model)
    # increment like counter
    video.no_likes += 1
    # commit to database
    db.add(video)
    db.commit()
    db.refresh(video)
    return {"status": 200}


def video_dislike(db: Session, video_int: str, user_id: int):
    """Adds a like to video"""
    # query the database for video
    video = get_video(db, video_int)
    user = get_user(db, user_id)
    # check if user has dislike before
    # check like status
    like_entry = check_like_dislike(db, video.video_id, user.user_id)
    # if user already liked before
    if like_entry and like_entry.like_dislike is False:
        return None
    # if user has liked before
    if like_entry and like_entry.like_dislike is True:
        like_entry.like_dislike = False
        # reduce likes by 1
        video.no_likes -= 1
        db.add(like_entry)
        db.commit()
        db.refresh(like_entry)
    # if not disliked before
    else:
        like_model = models.UserLikesDislikes(
            like_user_id=user.user_id, like_video_id=video.video_id, like_dislike=False
        )
        db.add(like_model)
        db.commit()
        db.refresh(like_model)
    # increment like counter
    video.no_dislikes += 1
    # commit to database
    db.add(video)
    db.commit()
    db.refresh(video)
    return {"status": 200}


# def get video
def get_video(db: Session, video_id: int):
    """
    get video from table video_library
    Args:
        - db: Session
        - video_id: int
    Returns:
        - Session query object
    """
    return db.query(models.Video).filter(models.Video.video_id == video_id).first()


def get_video_link(db: Session, video_link: str):
    """
    get video from video link
    """
    return db.query(models.Video).filter(models.Video.video_link == video_link).first()


def get_top_videos(db: Session, skip: int = 0, limit: int = 100):
    """
    Get top videos ordered by
    views

    Gets the top 10 videos
    """
    return (
        db.query(models.Video)
        .order_by(models.Video.views.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# def delete video
def delete_video(db: Session, video_id: int):
    """
    Delete from table video_library
    Please note: this does not delete from media storage
    Args:
        - db: Session
        - video_id: int

    Returns:
        - status: bool
    """
    db_video = db.query(models.Video).filter(models.Video.video_id == video_id).first()
    try:
        db.delete(db_video)
        db.commit()
        return True
    except Exception as e:
        print(f"Could not delete video={video_id}: {e}")
        return False


# def create comment
def create_comment(db: Session, comment: str, video_id: int, user_id: int):
    """
    Adds comment to `comments` table
    Adds to Comment model.
    Attributes:
        - comment_id: int, primary, index
        - comment_user_id: int,
        - comment_content: string,
        - ts_comment: datetime

    Args:
        - db: Session
        - comment: schemas.Comment

    Returns:
        - session object
    """
    db_comment = models.Comment(
        comment_user_id=user_id,
        comment_video_id=video_id,
        comment_content=comment,
        ts_comment=get_timestamp_now(),
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


# def get comments of video
def get_comments(db: Session, video_id: int):
    """
    Get all comments for video from video_id from `comments` table
    Args:
        - db: Session
        - video_id: int

    Returns:
        - Session object all
    """
    return (
        db.query(models.Comment)
        .filter(models.Comment.comment_video_id == video_id)
        .limit(10)
        .all()
    )


# def change comment
def update_comment(db: Session, req_comment_id: int, new_content: str):
    """
    Update comment with new content
    Args:
        - db: Session
        - req_comment_id: int

    Returns:
        - Session object
    """
    db_comment = (
        db.query(models.Comment)
        .filter(models.Comment.comment_id == req_comment_id)
        .first()
    )
    db_comment.comment_content = new_content
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


# def delete comment
def delete_comment(db: Session, comment_id: int):
    """
    Delete comment from comments table
    Args:
        - db: Session
        - comment_id: int

    Returns:
        - Status: bool
    """
    db_comment = (
        db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()
    )
    try:
        db.delete(db_comment)
        db.commit()
        return True
    except Exception as e:
        print(f"Could not delete user={comment_id}: {e}")
        return False


def get_profile_bool(db: Session, username: str):
    """Gets profile picture flag

    Args:
        db: Database
        username: Username to check

    Returns:
        Bool value of User.profile_picture
    """
    return (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
        .profile_picture
    )
