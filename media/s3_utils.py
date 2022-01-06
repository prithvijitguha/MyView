"""Module to interact with s3 storage"""

# pylint: disable=import-error

import os
import boto3


from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()


def upload_file(file_object, bucket, object_name):
    """Upload a file to an S3 bucket

    Args:
        - file_object: File to upload
        - bucket: Bucket to upload to
        - object_name: S3 object name. If not specified then file_name is used
    Returns:
        - True if file was uploaded, else False
    """
    # Upload the file
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("aws_access_key_id"),
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
    )

    try:
        s3_client.put_object(Body=file_object, Bucket=bucket, Key=object_name)
    except ClientError as s3_error:
        print(f"Could not upload{object_name}: {s3_error}")
        return False
    return True
