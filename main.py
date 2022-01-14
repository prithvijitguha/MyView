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

import os

from fastapi import FastAPI, Request, Depends, Response
from fastapi import HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from jwt.jwt_utils import get_current_user, create_access_token


from crud import crud
from models import models
from schemas import schemas
from media import s3_utils
from db.database import get_db, engine
from utils import utils

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

# static files directory for javascript and css
app.mount("/static", StaticFiles(directory="static"), name="static")

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
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRES"))


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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    HomePage
    """
    # checks if user if logged in
    active_user = get_current_user
    if active_user:
        return templates.TemplateResponse(
            "index.html", context={"request": request, "active_user": active_user}
        )
    else:
        return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """
    Upload page
    """
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload_file")
async def upload_file(
    video_file: UploadFile = File(...),
    # pylint: disable=unused-argument
    thumbnail: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload file to s3
    Only accepts video file types.
    Args:
        - video_file: UploadFile
    Returns:
        - Status 200 if success, else 304 invalid type
    """
    if video_file.content_type in ["video/mp4", "video/x-m4v", "video/*"]:
        # upload to s3
        try:
            # upload video
            data = video_file.file._file
            filename = video_file.filename
            bucket = os.environ.get("bucket_name")
            new_video_name = utils.create_video_name(filename)
            folder_name = os.environ.get("folder_name")
            destination = f"{folder_name}/{new_video_name}"
            s3_utils.upload_file(data, bucket, destination)
            # upload thumbnail
            # data_tn = thumbnail.file._file
            # filename_tn = thumbnail.file.filename
            # new_tn_name = utils.create_video_name(filename_tn)
            # folder_name_tn = os.environ.get("folder_name_tn")
            # destination_tn = f"{folder_name_tn}/{new_tn_name}"
            # s3_utils.upload_file(data_tn, bucket, destination_tn)
        except Exception as e:
            print(f"Could not upload {filename}: {e}")
            return {"status": 124}
        # add entry to database
        try:
            # create schema according to video
            # schemas.Video()
            pass
            # TODO
        # crud.add_video(db=db,video= )

        except Exception as e:
            print(f"Could not make entry {filename}: {e}")
            return {"status": 125}

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
    Args:
        - email: str = Form(...)
        - password: str = Form(...)
    """
    # check if user is present
    user_status = crud.authenticate_user_email(db, email=email, password=password)
    # if username and password matches redirect to homepage
    if user_status:
        # create access token
        # set the cookie and return it
        token = await create_access_token(data={"sub": email})
        response.set_cookie("session", token)
        return templates.TemplateResponse("index.html", context={"request": request})
    # else provide error message
    else:
        context = {
            "request": request,
            "message": "Email or Password is incorrect",
            "tag": "warning",
        }
        return templates.TemplateResponse("login.html", context=context)


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
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Regiser Post Page
    Args:
        - username: str = Form(...)
        - password: str = Form(...)
        - email: str = Form(...)

    """
    # get the details
    user = schemas.UserCreate(username=username, email=email, password=password)
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
