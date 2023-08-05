"""Module housing API routes."""
import uvicorn
from fastapi import FastAPI

from registration_app.orm.database import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    """Test root."""
    return {"message": "Hello World"}


def launch():
    """Entrypoint for the backend."""
    # TODO move to environment variables
    uvicorn.run(app=app, host="127.0.0.1", port=5000, log_level="info")
