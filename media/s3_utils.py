"""Module to interact with s3 storage"""

# pylint: disable=import-error

import os
import boto3


from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()


def upload_file(file_name, bucket, object_name):
    """Upload a file to an S3 bucket

    Args:
        - file_name: File to upload
        - bucket: Bucket to upload to
        - object_name: S3 object name. If not specified then file_name is used
    Returns:
        - True if file was uploaded, else False
    """
    # access s3
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("aws_access_key_id"),
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
    )

    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as s3_error:
        print(f"Could not upload{file_name}: {s3_error}")
        return False
    return True
