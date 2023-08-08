"""Non-DB backed models."""
from typing import Literal

from pydantic import BaseModel
from registration_app.orm.models import UserInfo


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

class UserProfileResponse(BaseModel):
    """User profile information returned as a response from the profile endpoint"""
    # TODO better docstrings here?:w
    user_basics: dict
    """Basic information of the user, specifically the first name, last name, and thumbnail"""

    user_sessions: list
    """Information on the user's sessions, specifically the IP, country, time, and browser of previous sessions. Also includes session_id since it is the primary key."""
