provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS Region"
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

resource "aws_s3_bucket" "prompts_bucket" {
  bucket = var.bucket_name

  tags = {
    Name        = "Agent Prompts"
    Environment = "Production"
  }
}

resource "aws_s3_bucket_versioning" "prompts_versioning" {
  bucket = aws_s3_bucket.prompts_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "bucket_config" {
  bucket = aws_s3_bucket.prompts_bucket.id

  rule {
    id = "archive-old-versions"
    status = "Enabled"

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      noncurrent_days = 365
    }
  }
}

output "bucket_domain_name" {
  value = aws_s3_bucket.prompts_bucket.bucket_domain_name
}
