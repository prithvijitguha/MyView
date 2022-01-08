"""Utils functions to be used in main"""

import hashlib
import os


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
