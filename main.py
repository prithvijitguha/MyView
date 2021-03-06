"""
MyView all views saved here
"""
# flake8: noqa:E501
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=protected-access
# pylint: disable=no-else-return
# pylint: disable=broad-except
# pylint: disable=using-constant-test
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=redefined-outer-name


import os

from html import escape
from typing import Optional, Union
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, Request, Depends, Response, status
from fastapi import HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from jwt.jwt_utils import get_current_user_optional, create_access_token


from crud import crud
from models import models
from schemas import schemas
from media import s3_utils
from db.database import get_db, engine
from utils import utils

models.Base.metadata.create_all(bind=engine)

description = """MyView is an online video sharing platform with open source in mind"""

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title="MyView",
    description=description,
    version="0.1.0",
    contact={
        "name": "Prithvijit Guha",
        "url": "https://github.com/prithvijitguha",
    },
    license_info={
        "name": "BSD 3-Clause License",
        "url": "https://github.com/prithvijitguha/MyView/blob/master/LICENSE",
    },
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8000/",
    "*",
]

# static files directory for javascript and css
app.mount("/static", StaticFiles(directory="./static"), name="static")


# html templates directory
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

# url to get tokens from

JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGO = os.environ.get("JWT_ALGO")


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Function to create a user
    First check if user exists.
    Args:
        - user: schemas.UserCreate
        - db: Session

    Returns:
        - db_user

    Raises:
        - HTTPException if email already registered

    """
    db_user = crud.get_user_by_email(db, email=user.email)
    # check if email already exists
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Function to read user table.
    Check if user exists.
    Raise error if not found
    Args:
        - user_id: int
        - db: Session
    Returns:
        - user
    Raises:
        - HTTPException if user not found
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/get_top_videos/{skip}/{limit}")
def get_videos(
    skip: Union[int, str] = 0,
    limit: Union[int, str] = 10,
    db: Session = Depends(get_db),
):
    """Function to get top videos from database

    Args:
        db: Database
        skip: video of videos to start
        limit: video of videos to end

    Returns:
        Array of videos ordered by views
    """
    return crud.get_top_videos(db, skip, limit)


@app.get("/get_profile_picture/{username}")
def get_profile_picture_bool(
    username: str,
    db: Session = Depends(get_db),
):
    """Gets the profile picture bool flag

    Args:
        username: Username to check
        db: Database

    Returns:
        boolean value of Bool value of User.profile_picture
    """
    return crud.get_profile_bool(db, username)


@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    active_user: Optional[schemas.UserBase] = Depends(get_current_user_optional),
    #    db: Session = Depends(get_db),
):
    """
    HomePage
    Args:
        - request: Request
        - active_user: Optional[schemas.User] = Depends(get_current_user)

    Returns:
        - index.html
        - Optional: active_user
    """
    # Get top videos
    # query top videos by views
    # sanitize active_user
    if active_user:
        active_user = utils.sanitize_active_user(active_user)

    request = utils.sanitize_request(request)

    context = {
        "request": request,
        "active_user": active_user,
    }

    return templates.TemplateResponse(
        "index.html",
        context=context,
    )


@app.get("/video/{video_link}")
def read_video(
    request: Request,
    video_link: str,
    db: Session = Depends(get_db),
    active_user: Optional[schemas.User] = Depends(get_current_user_optional),
):
    """
    Serves Video link
    Increments view by 1
    Args:
        -request: Request,
        - video_link: str,
        - db: Session = Depends(get_db),
        - active_user: Optional[schemas.User] = Depends(get_current_user_optional),

    Returns:
        - video.html template with context
    """
    # sanitize
    if active_user:
        active_user.username = escape(active_user.username)

    video = crud.get_video_link(db, video_link)
    cloud_url = os.environ.get("cloud_url")
    folder_name = os.environ.get("folder_name")
    video_url = f"{cloud_url}/{folder_name}"
    crud.increase_view(db, video.video_id, active_user)

    # get all comments
    comments = crud.get_comments(db, video_id=video.video_id)

    # get username
    def get_username(user_id):
        return crud.get_username(db, user_id)

    # get profile picture
    def get_profile(username):
        """
        Function to get
        bool of profile_picture of
        User
        """
        return (
            db.query(models.User)
            .filter(models.User.username == username)
            .first()
            .profile_picture
        )

    return templates.TemplateResponse(
        "video.html",
        context={
            "request": request,
            "video_url": video_url,
            "active_user": active_user,
            "video": video,
            "video_link": video_link,
            "comments": comments,
            "get_profile": get_profile,
            "get_username": get_username,
        },
    )


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(
    request: Request, active_user: schemas.User = Depends(get_current_user_optional)
):
    """
    Upload page
    """
    # if user is not logged in
    if not active_user:
        # url for login
        url = app.url_path_for("login")
        # return url
        response = RedirectResponse(url=url)
        # set found status code
        response.status_code = status.HTTP_302_FOUND
        return response

    # sanitize active_user
    active_user = utils.sanitize_active_user(active_user)

    return templates.TemplateResponse(
        "upload.html", context={"request": request, "active_user": active_user}
    )


@app.post("/upload_file", dependencies=[Depends(utils.valid_content_length)])
async def upload_file(
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    video_file: UploadFile = File(...),
    videoName: str = Form(...),
    videoLength: str = Form(...),
    videoHeight: int = Form(...),
    videoWidth: int = Form(...),
    # pylint: disable=unused-argument
    thumbnail: UploadFile = File(...),
    db: Session = Depends(get_db),
    active_user: schemas.User = Depends(get_current_user_optional),
    videoDescription: Optional[str] = Form(None),
    videoCategories: Optional[str] = Form(None),
):
    """
    Upload file to s3
    Only accepts video file types.
    Limit file uploads to 100 mb
    Args:
        - video_file: UploadFile
    Returns:
        - Status 200 if success, else 304 invalid type
    """
    # sanitize input
    videoName = escape(videoName)
    videoLength = escape(videoLength)
    if videoDescription:
        videoDescription = escape(videoDescription)
    if videoCategories:
        videoCategories = escape(videoCategories)
    file_size = 10_00_00_000

    real_file_size = 0
    # pylint: disable="consider-using-with"
    temp = NamedTemporaryFile()
    # check file size
    for chunk in video_file.file:
        real_file_size += len(chunk)
        if real_file_size > file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too large"
            )
        temp.write(chunk)
    temp.close()

    # pylint: disable=too-many-locals
    if video_file.content_type in ["video/mp4", "video/x-m4v", "video/mpeg4"]:

        # upload to s3
        try:
            # upload video
            # bring the file reader to start position
            await video_file.seek(0)
            # convert to bytes
            data = video_file.file
            # get filename
            filename = video_file.filename
            file_format = video_file.content_type
            # extract extension from file
            bucket = os.environ.get("bucket_name")
            new_video_name = utils.create_video_name(filename)
            folder_name = os.environ.get("folder_name")
            destination = f"{folder_name}/{new_video_name}"
            s3_utils.upload_file(data, bucket, destination)
            # upload thumbnail
            thumbnail_drive = os.environ.get("thumbnail_drive")
            thumbnail_data = thumbnail.file._file
            thumbnail.filename = new_video_name
            thumbnail_destination = f"{thumbnail_drive}/{thumbnail.filename}"
            s3_utils.upload_file(thumbnail_data, bucket, thumbnail_destination)
        except Exception as e:
            print(f"Could not upload {filename}: {e}")
            return {"status": 124}
        # add entry to database
        try:
            # create instance of video schemas
            # add parameters
            username = active_user.username
            video = schemas.Video(
                video_username=username,
                video_link=new_video_name,
                video_name=videoName,
                video_height=videoHeight,
                video_width=videoWidth,
                file_format=file_format,
                categories=videoCategories,
                description=videoDescription,
                length=videoLength,
            )
            # pass it to crud function
            crud.add_video(db, video)
        except Exception as e:
            print(f"Could not make entry {filename}: {e}")
            return {"status": 125}
        # url for homepage
        url = app.url_path_for("home")
        response = RedirectResponse(url=url)
        # set found status code
        response.status_code = status.HTTP_302_FOUND
        return response

    else:
        return {"Invalid file type": 304}


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Login Page
    """
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    email: str = Form(...),
    password: str = Form(...),
):
    """
    Login Page Post
    Logs user in and creates cookie
    Args:
        - request: Request,
        - response: Response,
        - db: Session = Depends(get_db),
        - email: str = Form(...),
        - password: str = Form(...),

    Returns:
        - index.html: if user credentials are valid
        - login.html: if user credentials are invalid
    """
    # check if user is present
    user_status = crud.authenticate_user_email(db, email=email, password=password)
    # if username and password matches redirect to homepage
    if user_status:
        # create access token
        token = await create_access_token(data={"sub": email})
        # url for homepage
        url = app.url_path_for("home")
        # return url
        response = RedirectResponse(url=url)
        # set found status code
        response.status_code = status.HTTP_302_FOUND
        response.set_cookie("session", token)
        return response

    # else provide error message
    else:
        login_context = {
            "request": request,
            "message": "Email or Password is incorrect",
            "tag": "warning",
        }
        return templates.TemplateResponse("login.html", context=login_context)


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Register page

    """
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    profile_picture: UploadFile = File(None),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Regiser Post Page
    Args:
        - request: Request
        - username: str = Form(...)
        - password: str = Form(...)
        - profile_picture: UploadFile = File(None)
        - email: str = Form(...)
        - db: Session = Depends(get_db)

    Returns:
        - register.html: if name already in use
        - login.html: if successly registered

    """
    # sanitize input
    username = escape(username)
    password = escape(password)
    email = escape(email)

    profile_bool = False
    # if profile picture is present then upload
    if profile_picture and profile_picture.content_type in [
        "image/jpeg",
        "image/jpg",
        "image/png",
    ]:
        bucket = os.environ.get("bucket_name")
        profile_folder = os.environ.get("profile_folder")
        profile_pic = profile_picture.file._file
        new_profile_name = username
        destination = f"{profile_folder}/{new_profile_name}"
        s3_utils.upload_file(profile_pic, bucket, destination)
        profile_bool = True
    # otherwise none
    # get the details
    user = schemas.UserCreate(
        username=username, email=email, password=password, profile_picture=profile_bool
    )
    # first check if user exists
    # #if user exists return error
    username_check = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    email_check = db.query(models.User).filter(models.User.email == user.email).first()
    if username_check or email_check:
        error_context = {
            "request": request,
            "message": "Email or Username already in use",
            "tag": "warning",
        }
        return templates.TemplateResponse("register.html", context=error_context)
    # create the schema to carry it
    # create user
    create_user(db=db, user=user)
    success_context = {
        "request": request,
        "message": "Successfully registered",
        "tag": "success",
    }
    return templates.TemplateResponse("login.html", context=success_context)


@app.get("/logout")
def logout(response: Response, request: Request):
    """
    Logs user out of session.
    Deletes cookie

    Args:
        - response: Response
        - request: Request

    Returns:
        - response - index.html and delete cookie session
    """
    success_context = {
        "request": request,
        "message": "Successfully Logged Out",
        "tag": "success",
    }
    response = templates.TemplateResponse("index.html", context=success_context)
    response.delete_cookie("session")
    return response


@app.get("/search")
def search_video(request: Request, search_query: str, db: Session = Depends(get_db)):
    """
    Search Video
    Args:
        - search_query
        - Depends(get_db)

    Returns:
        - queried objects
    """
    # sanitize input
    search_query = escape(search_query)

    query_videos = (
        db.query(models.Video)
        .filter(models.Video.video_name.contains(search_query))
        .limit(10)
        .all()
    )

    thumbnail_drive = os.environ.get("thumbnail_drive")
    cloud_url = os.environ.get("cloud_url")
    thumbnail_url = f"{cloud_url}/{thumbnail_drive}"
    profile_folder = os.environ.get("profile_folder")
    profile_picture_url = f"{cloud_url}/{profile_folder}"

    def get_profile(username):
        """
        Function to get
        bool of profile_picture of
        User
        """
        return (
            db.query(models.User)
            .filter(models.User.username == username)
            .first()
            .profile_picture
        )

    return templates.TemplateResponse(
        "results.html",
        context={
            "request": request,
            "videos": query_videos,
            "get_profile": get_profile,
            "profile_picture_url": profile_picture_url,
            "thumbnail_url": thumbnail_url,
        },
    )


@app.post("/like")
async def like_video(
    request: Request,
    active_user: Optional[schemas.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """
    like url
    """
    if not active_user:
        # TODO replace with redirect
        return {"Error": "Not logged in"}
    data = await request.json()

    # sanitize input
    video_id = escape(data["video_id"])
    active_user.username = escape(active_user.username)

    result = crud.video_like(db, video_int=video_id, user_id=active_user.user_id)
    return result


@app.post("/dislike")
async def dislike_video(
    request: Request,
    active_user: Optional[schemas.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """
    dislike url
    """
    if not active_user:
        # TODO replace with redirect
        return {"Error": "Not logged in"}
    data = await request.json()

    # sanitize input
    video_id = escape(data["video_id"])
    active_user.username = escape(active_user.username)

    result = crud.video_dislike(db, video_int=video_id, user_id=active_user.user_id)
    return result


@app.post("/comment/add")
async def add_comment(
    request: Request,
    active_user: Optional[schemas.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """
    Comment url to add comments
    """
    if not active_user:
        # TODO replace with redirect
        return {"Error": "Not logged in"}
    data = await request.json()

    # sanitize input
    comment_data = escape(data["comment_data"])
    video_id = escape(data["video_id"])
    # sanitize active_user
    if active_user:
        active_user = utils.sanitize_active_user(active_user)

    result = crud.create_comment(db, comment_data, video_id, active_user.user_id)
    return result


@app.delete("/comment/delete")
async def delete_comment(
    request: Request,
    active_user: Optional[schemas.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """
    Function to delete comment
    """
    if not active_user:
        # TODO replace with redirect
        return {"Error": "Not logged in"}
    comment_id = await request.json()
    comment_id = escape(comment_id)
    comment_id = int(comment_id)
    crud.delete_comment(db, comment_id)
    return {"Success": "comment deleted"}


@app.get("/profile")
def profile_page(
    request: Request,
    active_user: schemas.User = Depends(get_current_user_optional),
):
    """URL to serve profile page

    Args:
        request: HTTP request
        active_user: Current logged in user

    Returns:
        template: profile.html
        context: dict of request and active_user

    If user not logged in redirects to login page
    """
    if not active_user:
        # url for login
        url = app.url_path_for("login")
        # return url
        response = RedirectResponse(url=url)
        # set found status code
        redirect_code = status.HTTP_302_FOUND
        response.status_code = redirect_code
        return response

    context = {
        "request": request,
        "active_user": active_user,
    }

    return templates.TemplateResponse("profile.html", context=context)


@app.get("/get_uploaded_videos/{username}/{skip}/{limit}")
def get_uploaded_videos(
    username: str,
    active_user: Optional[schemas.User] = Depends(get_current_user_optional),
    skip: Union[int, str] = 0,
    limit: Union[int, str] = 5,
    db: Session = Depends(get_db),
):
    """Function to get top videos from database

    Args:
        db: Database
        skip: video of videos to start
        limit: video of videos to end

    Returns:
        Array of videos ordered by views
    """
    if active_user.username != username:
        raise HTTPException(
            status_code=400, detail="Current User not matching the user searched for"
        )
    return crud.get_top_videos_by_user(db, username, skip, limit)


@app.delete("/delete_video/{username}/{video_id}")
def delete_video(
    username: str,
    video_id: int,
    active_user: Optional[schemas.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """Delete Video API

    Args:
        username: Username of video to delete
        video_id: Id of video to be delete
        active_user: Current user
        db: Database

    Returns:
        status of success or failure

    Raises:
        if active_user and username do not match
    """
    if active_user.username != username or not active_user.admin:
        raise HTTPException(status_code=400, detail="Unauthorized Delete Request")
    status = crud.delete_video(db, video_id)
    return status
