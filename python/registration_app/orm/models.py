"""Module housing all the models stored in the application."""
import datetime
from random import randint
from typing import Optional
from uuid import UUID, uuid4

from pydantic import EmailStr
from pydantic import Field as PydanticField
from pydantic import SecretStr, ValidationError, validator
from pydantic.networks import IPvAnyAddress
from sqlmodel import Field, SQLModel


class UserInfoBase(SQLModel):
    """Class housing fields shared across all representation of `User`s."""

    username: str = Field(primary_key=True)
    first: str
    last: str


class UserInfo(UserInfoBase, table=True):
    """Information about a particular user, as stored in the database."""

    # TODO Put this in
    thumbnail: bytes = Field(
        default_factory=lambda: bytes([randint(1, 3) for _ in range(1024)])
    )


class UserInfoCreate(UserInfoBase):
    """Representation of the required fields needed to create a `UserInfo` entry."""

    email: EmailStr
    password: SecretStr = PydanticField(min_length=6)


# TODO add browser history
class SessionInfo(SQLModel, table=True):
    """Creates user session information table"""

    session_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(foreign_key="userinfo.username")
    time: datetime.datetime
    ip: str
    country: str
    browser: str

    @validator("ip")
    def ensure_ip_is_valid(cls, ip: str):
        """Ensure that the ip field is a valid IP address."""
        IPvAnyAddress.validate(ip)
        return ip

    @validator("browser")
    def ensure_browser_is_valid(cls, browser: str):
        valid_browsers = [
            "Firefox",
            "Seamonkey",
            "Chrome",
            "Chromium",
            "Safari",
            "Opera",
            "Other",
        ]
        if browser in valid_browsers:
            return browser
        else:
            raise ValidationError
