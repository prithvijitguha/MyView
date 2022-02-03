"""
Tests for s3 utils module
"""
# flake8: noqa:E712
# pylint: disable=import-error

from moto import mock_s3
from media import s3_utils


@mock_s3
def test_upload_file():
    """
    Test s3 upload file
    """
    test_file_body = "test object"
    test_bucket = "test_bucket"
    test_file_name = "test_file_name"
    result = s3_utils.upload_file(test_file_body, test_bucket, test_file_name)
    assert result is False
