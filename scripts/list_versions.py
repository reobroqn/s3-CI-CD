import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET_NAME")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

def list_versions(prefix="prompts/"):
    """List all versions of prompts in S3."""
    print(f"Listing versions in '{S3_BUCKET}' for prefix '{prefix}'...")

    try:
        response = s3_client.list_object_versions(Bucket=S3_BUCKET, Prefix=prefix)

        if "Versions" in response:
            current_key = None
            for v in response["Versions"]:
                if v["Key"] != current_key:
                    print(f"\nFile: {v['Key']}")
                    current_key = v["Key"]

                is_latest = " (LATEST)" if v["IsLatest"] else ""
                print(f"  - Version: {v['VersionId']} | Modified: {v['LastModified']}{is_latest}")
        else:
            print("No versions found.")

    except ClientError as e:
        print(f"Error listing versions: {e}")

if __name__ == "__main__":
    if not S3_BUCKET:
        print("Error: S3_BUCKET_NAME environment variable not set.")
    else:
        list_versions()
