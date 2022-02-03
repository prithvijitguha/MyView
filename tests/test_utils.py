"""Test utils module"""

from utils import utils


def test_video_name():
    """
    Test Video Name
    """
    hashed_name = utils.create_video_name("test_video_name")
    assert hashed_name
