from fastmcp import FastMCP
from mcp_server.s3_client import S3Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("S3 Prompts Server")

# Initialize S3 Client
s3_client = S3Client()

@mcp.tool
def get_prompt(key: str, version: str = None) -> str:
    """
    Get a prompt from S3.

    Args:
        key: The path to the prompt file in S3 (e.g., 'prompts/agent/system.txt')
        version: Optional version ID to fetch a specific version
    """
    content = s3_client.get_prompt(key, version)
    if content is None:
        return f"Error: Prompt '{key}' not found."
    return content

@mcp.tool
def list_prompts(prefix: str = "prompts/") -> str:
    """
    List available prompts in S3.

    Args:
        prefix: Optional prefix to filter prompts (default: 'prompts/')
    """
    prompts = s3_client.list_prompts(prefix)
    if not prompts:
        return "No prompts found."
    return "\n".join(prompts)

@mcp.tool
def list_prompt_versions(key: str) -> str:
    """
    List all versions of a specific prompt.

    Args:
        key: The path to the prompt file
    """
    versions = s3_client.list_versions(key)
    if not versions:
        return f"No versions found for '{key}'."

    result = [f"Versions for {key}:"]
    for v in versions:
        latest = " (Latest)" if v["IsLatest"] else ""
        result.append(f"- {v['VersionId']} | {v['LastModified']}{latest}")

    return "\n".join(result)

if __name__ == "__main__":
    mcp.run()
