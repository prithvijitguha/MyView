"""Write your tests here"""
# flake8: noqa:E501
# pylint: disable=import-error
# pylint: disable=invalid-name
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db.database import Base, get_db


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


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
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
