"""Module housing API routes."""
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    """Test root."""
    return {"message": "Hello World"}

def launch():
    """Entrypoint for the backend."""
    # TODO move to environment variables
    uvicorn.run(app=app, host="127.0.0.1", port=5000, log_level="info")