import os
from pathlib import Path

from dotenv import load_dotenv


def load_env():
    """Load the environment variables of the application."""
    load_dotenv(os.environ["FASTAPI_ENV_PATH"])
