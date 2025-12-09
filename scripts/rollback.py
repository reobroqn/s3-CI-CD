import os
import sys

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET_NAME")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def rollback_prompt(key: str, version_id: str):
    """
    Rollback a prompt to a specific version.
    In S3, 'rollback' effectively means copying a previous version
    to be the new latest version.
    """
    print(f"Rolling back '{key}' to version '{version_id}'...")

    try:
        # Copy the specific version to the same key, making it the new latest
        copy_source = {"Bucket": S3_BUCKET, "Key": key, "VersionId": version_id}

        s3_client.copy_object(Bucket=S3_BUCKET, Key=key, CopySource=copy_source)
        print(f"✓ Successfully rolled back '{key}' to version '{version_id}'.")
        print("This is now the latest version.")

    except ClientError as e:
        print(f"Error rolling back: {e}")


if __name__ == "__main__":
    if not S3_BUCKET:
        print("Error: S3_BUCKET_NAME environment variable not set.")
        sys.exit(1)

    if len(sys.argv) != 3:
        print("Usage: python scripts/rollback.py <key> <version_id>")
        print("Example: python scripts/rollback.py prompts/agent/system.txt v123456")
        sys.exit(1)

    key = sys.argv[1]
    version_id = sys.argv[2]

    rollback_prompt(key, version_id)
