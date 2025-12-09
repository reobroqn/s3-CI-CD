import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET_NAME")

s3_client = boto3.client(
    "s3",
)


def download_prompts(prefix="prompts/", local_dir="."):
    """Download prompt files from S3 to local directory."""
    print(f"Downloading prompts from '{S3_BUCKET}' to '{local_dir}'...")

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=prefix):
            if "Contents" in page:
                for obj in page["Contents"]:
                    s3_key = obj["Key"]
                    local_path = os.path.join(local_dir, s3_key)

                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)

                    print(f"Downloading {s3_key}...")
                    s3_client.download_file(S3_BUCKET, s3_key, local_path)
                    print(f"✓ Downloaded {s3_key}")
            else:
                print("No prompts found.")

    except ClientError as e:
        print(f"Error downloading prompts: {e}")


if __name__ == "__main__":
    if not S3_BUCKET:
        print("Error: S3_BUCKET_NAME environment variable not set.")
    else:
        download_prompts()
