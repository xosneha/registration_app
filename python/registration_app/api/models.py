"""Non-DB backed models."""
from typing import Literal

from pydantic import BaseModel


class JWTToken(BaseModel):
    """Token returned by backend upon successful login."""

    access_token: str
    """Encoded JWT token."""

    token_type: Literal["bearer"] = "bearer"
    """The type of the token. Always 'bearer'"""


class TokenData(BaseModel):
    """Data encoded in the JWT."""

    username: str
    """Username of user who is logged in."""
