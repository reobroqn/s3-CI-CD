import glob
import json
import os

import pytest

PROMPTS_DIR = "prompts"


def test_prompts_directory_exists():
    assert os.path.exists(PROMPTS_DIR)
    assert os.path.isdir(PROMPTS_DIR)


def test_json_files_are_valid():
    """Ensure all JSON files in the prompts directory are valid JSON."""
    json_files = glob.glob(f"{PROMPTS_DIR}/**/*.json", recursive=True)

    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {file_path}: {e}")


def test_required_agent_prompts_exist():
    """Ensure critical agent prompts exist."""
    agent_dir = os.path.join(PROMPTS_DIR, "agent")
    required_files = ["system.txt", "instructions.txt"]

    for filename in required_files:
        path = os.path.join(agent_dir, filename)
        assert os.path.exists(path), f"Missing required prompt file: {filename}"


def test_file_encoding_is_utf8():
    """Ensure all text files are UTF-8 encoded."""
    text_files = glob.glob(f"{PROMPTS_DIR}/**/*.txt", recursive=True)
    text_files.extend(glob.glob(f"{PROMPTS_DIR}/**/*.json", recursive=True))

    for file_path in text_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                f.read()
        except UnicodeDecodeError:
            pytest.fail(f"File {file_path} is not valid UTF-8")
