import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = os.environ.get("FASTAPI_ENV_PATH", Path(__file__).parent.parent.parent / "docker" / ".env")


def load_env():
    """Load the environment variables of the application."""
    load_dotenv(ENV_PATH)
