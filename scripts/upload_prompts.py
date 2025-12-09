import glob
import mimetypes
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION,
)


def upload_prompts(directory="prompts"):
    """Recursively upload prompt files to S3."""
    print(f"Uploading prompts from '{directory}' to bucket '{S3_BUCKET}'...")

    files = glob.glob(f"{directory}/**/*", recursive=True)

    for file_path in files:
        if os.path.isfile(file_path):
            # Convert Windows path to S3 key (forward slashes)
            s3_key = file_path.replace("\\", "/")

            content_type, _ = mimetypes.guess_type(file_path)
            content_type = content_type or "text/plain"

            try:
                print(f"Uploading {s3_key}...")
                with open(file_path, "rb") as f:
                    s3_client.put_object(
                        Bucket=S3_BUCKET, Key=s3_key, Body=f, ContentType=content_type
                    )
                print(f"✓ Uploaded {s3_key}")
            except ClientError as e:
                print(f"✗ Failed to upload {s3_key}: {e}")


if __name__ == "__main__":
    if not S3_BUCKET:
        print("Error: S3_BUCKET_NAME environment variable not set.")
    else:
        upload_prompts()
