"""Utils functions to be used in main"""
# pylint: disable=import-error
# flake8: noqa:E501
import hashlib
import os

from html import escape

from fastapi import Header


def create_video_name(video_name: str):
    """
    Takes a video name
    and creates a hash value for it
    Args:
        - video_name: str
    Returns
        - hashed_video: str
    """
    # convert to byte string
    salt = os.urandom(int(os.environ.get("salt")))
    byte_string = video_name.encode("utf-8")
    hash_object = hashlib.pbkdf2_hmac("sha256", byte_string, salt, 10000)
    hashed_video = hash_object.hex()
    return hashed_video


def sanitize_active_user(active_user):
    """
    sanitize active_user object
    """
    active_user.username = escape(active_user.username)
    active_user.email = escape(active_user.email)
    return active_user


def sanitize_request(request):
    """sanitize request"""
    # iterate through dict values
    # TODO add sanitization
    return request


async def valid_content_length(content_length: int = Header(..., lt=10_00_00_000)):
    """Check the header content_length
    ensure its smaller than 100mb"""
    return content_length
