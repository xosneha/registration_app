"""Module housing API routes."""
import re
from datetime import datetime, timezone
from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import load_only
from sqlmodel import select

from registration_app.api.models import (JWTToken, TokenData,
                                         UserProfileResponse)
from registration_app.authenticate import (create_access_token,
                                           create_user_in_ldap,
                                           decode_access_token,
                                           user_authenticate)
from registration_app.orm.database import create_db_and_tables, get_session
from registration_app.orm.models import SessionInfo, UserInfo, UserInfoCreate

app = FastAPI()
TOKEN_URL = "user_login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def get_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """
    Get the user initiating a request.

    :param token: The token attached to the request
    :return: The username of the user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not (data := decode_access_token(token)):
        raise credentials_exception
    return data


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    """Test root."""
    return {"message": "Hello World"}


@app.post(f"/{TOKEN_URL}", status_code=201, response_model=JWTToken)
async def user_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
):
    """Authenticate to the application."""
    if not user_authenticate(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # TODO Fix this
    session_info = generate_session_info(
        request=request, username=form_data.username, user_country="Fakestr"
    )
    with get_session() as session:
        session.add(SessionInfo.from_orm(session_info))
        session.commit()

    access_token = create_access_token(username=form_data.username)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get(f"/user_profile", status_code=200, response_model=UserProfileResponse)
async def user_profile(user: Annotated[TokenData, Depends(get_user)]):
    """Get user profile information from the db"""
    username = user.username
    with get_session() as session:
        user_basics = session.exec(
            select(UserInfo).where(UserInfo.username == username)
        )
        user_basics = user_basics.first()

        user_sessions = session.exec(
            select(SessionInfo)
            .where(SessionInfo.username == username)
            .options(load_only("time", "ip", "browser", "country"))
        )
        user_sessions = user_sessions.all()

    return {"user_basics": user_basics, "user_sessions": user_sessions}


# TODO Add user country to frontend
def generate_session_info(request: Request, username, user_country: str) -> SessionInfo:
    user_ip = request.client.host
    user_time = datetime.now(timezone.utc)
    browser = "Other"
    user_agent = request.headers["user-agent"]
    # See https://developer.mozilla.org/en-US/docs/Web/HTTP/Browser_detection_using_the_user_agent
    # for the list of browsers used
    if "Seamonkey" in user_agent:
        browser = "Seamonkey"
    elif "Firefox" in user_agent:
        browser = "Firefox"
    elif "Chromium" in user_agent:
        browser = "Chromium"
    elif "Chrome" in user_agent:
        edge_pattern = re.compile(["Edg.*.xyz"])
        if not edge_pattern.match(user_agent):
            browser = "Chrome"
    elif "Safari" in user_agent:
        browser = "Safari"
    elif "OPR" or "Opera" in user_agent:
        browser = "Opera"

    return SessionInfo(
        username=username,
        time=user_time,
        ip=user_ip,
        browser=browser,
        country=user_country,
    )


@app.post("/user_register", status_code=201, response_model=JWTToken)
async def user_registration(
    user: Annotated[UserInfoCreate, Body(embed=True)], request: Request
):
    result, reason = create_user_in_ldap(user=user)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{reason.capitalize()} is already taken",
        )
    # TODO Fix
    session_info = generate_session_info(
        request=request, username=user.username, user_country="fakeStr"
    )
    with get_session() as session:
        session.add(UserInfo.from_orm(user))
        session.commit()
        session.add(SessionInfo.from_orm(session_info))
        session.commit()
    access_token = create_access_token(username=user.username)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/token", response_model=str)
async def validate_token(current_user: Annotated[str, Depends(get_user)]):
    """Ensure user has a valid token."""
    return "You have a valid token!"
