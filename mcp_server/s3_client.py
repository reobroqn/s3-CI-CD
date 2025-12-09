import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


class S3Client:
    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def get_prompt(self, key: str, version_id: Optional[str] = None) -> Optional[str]:
        """
        Fetch a prompt from S3.
        If version_id is provided, fetches that specific version.
        Otherwise fetches the latest version.
        """
        try:
            params = {"Bucket": self.bucket_name, "Key": key}
            if version_id:
                params["VersionId"] = version_id

            response = self.s3.get_object(**params)
            return response["Body"].read().decode("utf-8")
        except ClientError as e:
            print(f"Error fetching prompt {key}: {e}")
            return None

    def list_prompts(self, prefix: str = "") -> List[str]:
        """List all available prompt keys in the bucket."""
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            if "Contents" not in response:
                return []
            return [obj["Key"] for obj in response["Contents"]]
        except ClientError as e:
            print(f"Error listing prompts: {e}")
            return []

    def list_versions(self, key: str) -> List[Dict[str, Any]]:
        """List all versions of a specific prompt."""
        try:
            response = self.s3.list_object_versions(Bucket=self.bucket_name, Prefix=key)
            versions = []
            if "Versions" in response:
                for v in response["Versions"]:
                    if v["Key"] == key:
                        versions.append(
                            {
                                "VersionId": v["VersionId"],
                                "LastModified": v["LastModified"].isoformat(),
                                "IsLatest": v["IsLatest"],
                            }
                        )
            return versions
        except ClientError as e:
            print(f"Error listing versions for {key}: {e}")
            return []
