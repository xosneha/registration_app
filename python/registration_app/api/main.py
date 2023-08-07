"""Module housing API routes."""
from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from registration_app.api.models import JWTToken
from registration_app.authenticate import (
    create_access_token,
    create_user_in_ldap,
    decode_access_token,
    user_authenticate,
)
from registration_app.orm.database import create_db_and_tables, get_session
from registration_app.orm.models import UserInfo, UserInfoCreate

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
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Authenticate to the application."""
    # TODO support email based authentication
    if not user_authenticate(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(username=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/user_register", status_code=201, response_model=JWTToken)
async def user_registration(user: Annotated[UserInfoCreate, Body(embed=True)]):
    if not create_user_in_ldap(user=user):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken",
        )
    with get_session() as session:
        session.add(UserInfo.from_orm(user))
        session.commit()
    access_token = create_access_token(username=user.username)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/token", response_model=str)
async def validate_token(current_user: Annotated[str, Depends(get_user)]):
    """Ensure user has a valid token."""
    return "You have a valid token!"
