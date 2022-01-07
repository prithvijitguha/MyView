"""
MyView all views saved here
"""

# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=protected-access
# pylint: disable=no-else-return

import os

from fastapi import FastAPI, Request, Depends
from fastapi import HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session


from crud import crud
from models import models
from schemas import schemas
from media import s3_utils
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """
    Upload page
    """
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload_file")
async def upload_file(video_file: UploadFile = File(...)):
    """
    Upload file to s3
    Only accepts video file types.
    Args:
        - video_file: UploadFile
    Returns:
        - Status 200 if success, else 304 invalid type
    """
    if video_file.content_type in ["video/mp4", "video/x-m4v", "video/*"]:
        data = video_file.file._file
        filename = video_file.filename
        bucket = os.environ.get("bucket_name")
        s3_utils.upload_file(data, bucket, filename)
        return {"status": 200}
    else:
        return {"Invalid file type": 304}


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Login Page
    """
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...)):
    """
    Login Page Post
    Args:
        - username: str = Form(...)
        - password: str = Form(...)

    """
    return {"username": username}
