"""
MyView all views saved here
"""
# flake8: noqa:E501
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=protected-access
# pylint: disable=no-else-return
# pylint: disable=broad-except
# pylint: disable=raise-missing-from

import os

from fastapi import FastAPI, Request, Depends, status
from fastapi import HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from sqlalchemy.orm import Session


from crud import crud
from models import models
from schemas import schemas
from media import s3_utils
from db.database import SessionLocal, engine
from utils import utils
from security import security

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

# path to get tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

cookie_sec = APIKeyCookie(name="session")


SECRET_KEY = os.environ.get("SECRET_KEY_JWT")
ALGORITHM = os.environ.get("JWT_ALGO")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRES"))


models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Connects to database
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    HomePage
    """
    return templates.TemplateResponse("index.html", {"request": request})


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
    # create access token
    data = {"token_type": "access_token", "sub": email}
    content = security.create_access_token(data=data)
    response = JSONResponse(content=content)
    response.set_cookie(data)

    if user_status:
        # check in user table for correct user name
        # check is UserHashed table for password match
        return templates.TemplateResponse("index.html", {"request": request})
    # else provide error message
    else:
        message = "Username or Password is incorrect"
        return {message: 141}


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Register page

    """
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register(
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
        return {"error": "email/username already taken"}
    # create the schema to carry it
    # create user
    create_user(db=db, user=user)
    return {"username": username}


async def get_current_user(
    token: str = Depends(cookie_sec), db: Session = Depends(get_db)
):
    """
    Get current user and check token status
    Args:
        token: str = Depends(cookie_sec)
        db:Session=Depends(get_db)

    Returns:
        user

    Raises:
        credentials_exception: HTTPException
        credentials_exception: if user is none
        JWT Error: credentials_exception
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


@app.get("/test")
def test(db: Session = Depends(get_db)):
    """
    Testing JWT
    """
    user = get_current_user(db=db)
    return user
