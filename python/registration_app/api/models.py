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

    user_basics: dict[str, str]
    """Basic information of the user
    :username: 
    :email:
    :first:
    :last: 
    """

    user_sessions: list
    """Information on the user's sessions, including
    :ip: User's IP in all sessions
    :country: User's country in all sessions
    :time: Date and time (UTC) that the user logged in/registered
    browser: User's browser 
    Also includes session_id since it is the primary key.
    """
