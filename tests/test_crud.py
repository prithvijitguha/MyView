"""Write your tests here"""
# flake8: noqa:E501
# pylint: disable=import-error
# pylint: disable=invalid-name
from crud import crud
from schemas import schemas
from tests.test_main import override_get_db


def test_hash():
    """
    Test hash function
    """
    hashed_password = crud.hash_password("test_password")
    assert isinstance(hashed_password, str)
    assert hashed_password != "test_password"


def test_compare_password():
    """
    Test hash compare password
    """
    hashed_password = crud.hash_password("test_password")
    assert crud.compare_password("test_password", hashed_password)


def test_create_user():
    """
    Test to create user
    """
    user = schemas.UserCreate(
        username="deadpool",
        email="deadpool@disney.com",
        password="disney@123",
        profile_picture=False,
    )
    db = next(override_get_db())
    status = crud.create_user(db, user)
    assert status


def test_get_user():
    """
    Test to authenticate user
    """
    db = next(override_get_db())
    assert crud.get_user(db, 1).username == "deadpool"


def test_get_username():
    """
    Test get username
    """
    db = next(override_get_db())
    assert crud.get_username(db, 1) == "deadpool"


def test_get_user_by_email():
    """
    Test get user by email
    """
    db = next(override_get_db())
    assert crud.get_user_by_email(db, "deadpool@disney.com").username == "deadpool"


def test_get_user_by_username():
    """
    Test get username
    """
    db = next(override_get_db())
    assert crud.get_user_by_username(db, "deadpool").user_id == 1


def test_get_user_id():
    """
    Test get user id
    """
    db = next(override_get_db())
    assert crud.get_user_id(db, "deadpool")
