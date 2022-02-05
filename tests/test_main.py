"""Write your tests here"""
# flake8: noqa:E501
# pylint: disable=import-error
# pylint: disable=invalid-name
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from moto import mock_s3


from main import app
from db.database import Base, get_db
from jwt.jwt_utils import get_current_user_optional
from schemas import schemas
from crud import crud
from utils.utils import valid_content_length

# Create local test.db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Function to override db
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    """
    Function to override get current user
    """
    current_user = schemas.User(
        username="deadpool",
        email="deadpool@disney.com",
        profile_picture=False,
        password="test",
        user_id=1,
        ts_joined=crud.get_timestamp_now(),
    )
    return current_user


def override_content_length():
    """
    Function to override content length header
    """
    return 0


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user_optional] = override_get_current_user
app.dependency_overrides[valid_content_length] = override_content_length

client = TestClient(app)


def test_read_home():
    """Check the index page for responses"""
    response = client.get("/")
    assert response.status_code == 200


def test_upload_page():
    """Check if response received from upload page"""
    response = client.get("/upload")
    assert response.status_code == 200


def test_register():
    """testing the create user function"""

    response = client.get("/register")
    assert response.status_code == 200, response.template

    response = client.post(
        "/register",
        data={
            "username": "test4",
            "email": "test4@example.com",
            "password": "test",
            "reconfirmPassword": "test",
            "profile_picture": None,
        },
    )

    assert response.status_code == 200, response.template


def test_login():
    """
    Test login
    """
    response = client.get("/login")
    assert response.status_code == 200, response.template

    response = client.post(
        "/login",
        data={
            "email": "test4@example.com",
            "password": "test",
        },
    )

    assert response.status_code == 302


def test_logout():
    """
    Test Logout
    """
    response = client.get("/logout")
    assert response.status_code == 200, response.template


@mock_s3
def test_upload_file():
    """
    Test Upload File
    """
    with open("./tests/test_data/test_video.mp4", "rb") as test_video, open(
        "./tests/test_data/test_thumbnail.jpg", "rb"
    ) as test_thumbnail:
        response = client.post(
            "/upload_file",
            files={
                "video_file": ("test_video", test_video, "video/mp4"),
                "thumbnail": ("test_thumbnail", test_thumbnail, "image/jpg"),
            },
            data={
                "videoName": "test_video",
                "videoLength": "100",
                "videoHeight": 720,
                "videoWidth": 1080,
                "videoDescription": "test_game_video_description",
                "videoCategories": "test_gaming",
            },
        )

    assert response.status_code in [302, 200]
