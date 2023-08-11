"""Module housing database connection and session management."""
import os

from sqlmodel import Session, SQLModel, create_engine

from registration_app import load_env
from registration_app.orm.models import *

load_env()

POSTGRES_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
ENGINE = create_engine(POSTGRES_URL)


def create_db_and_tables():
    """Instantiate the DB."""
    SQLModel.metadata.create_all(ENGINE)


def get_session():
    """Get a session to make DB queries."""
    return Session(ENGINE)
