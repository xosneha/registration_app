"""Module housing all the models stored in the application."""
import datetime
from typing import Optional

from pydantic import EmailStr, validator
from pydantic.networks import IPvAnyAddress
from sqlmodel import Field, SQLModel, create_engine


class UserInfo(SQLModel, table=True):
    """Creates basic user information table"""

    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: EmailStr
    first: str
    last: str
    thumbnail: str


# TODO add browser history
class SessionInfo(SQLModel, table=True):
    """Creates user session information table"""

    session_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="userinfo.user_id")
    time: datetime.datetime
    ip: str
    country: str
    # browser_history: list

    @validator("ip")
    def ensure_ip_is_valid(cls, ip: str):
        """Ensure that the ip field is a valid IP address."""
        IPvAnyAddress.validate(ip)
        return ip
