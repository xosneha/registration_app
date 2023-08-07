"""
Module handling authentication needs.
This includes:
    - Generating and decoding JWT tokens
    - Verifying credentials against LDAP server
    - Creating new users in LDAP server
"""
import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from jose import JWTError, jwt
from ldap3 import Connection, Server, Tls
from ldap3.core.exceptions import LDAPException as _LDAPException
from pydantic import ValidationError

from registration_app import load_env
from registration_app.api.models import TokenData
from registration_app.exceptions import LDAPException

load_env()


def create_access_token(username: str) -> str:
    """
    Create an access token to communicate with endpoints.

    :param username: The username of the user to create a token for.
    :return: An encoded JWT.
    """
    expire = datetime.utcnow() + timedelta(
        minutes=int(os.environ["FASTAPI_TOKEN_EXPIRY_MINUTES"])
    )
    to_encode = TokenData(username=username).dict() | {
        "exp": expire,
        "salt": secrets.token_hex(8),
    }
    return jwt.encode(
        to_encode,
        os.environ["FASTAPI_TOKEN_SECRET"],
        algorithm=os.environ["FASTAPI_TOKEN_ALGORITHM"],
    )


def decode_access_token(token: str) -> Optional[TokenData]:
    """
    Decode a JWT token.

    :param token: The token to decode.
    :return: The token data, if it was able to be decoded, None otherwise.
    """
    try:
        payload = jwt.decode(
            token,
            os.environ["FASTAPI_TOKEN_SECRET"],
            algorithms=[os.environ["FASTAPI_TOKEN_ALGORITHM"]],
        )
        payload.pop("exp", None)
        payload.pop("salt", None)
        return TokenData(**payload)
    except (JWTError, ValidationError):
        return None


def user_authenticate(username: str, password: str) -> bool:
    """
    Authenticate user against LDAP.

    :param username: The username of the user attempting to authenticate.
    :param password: The password of the authenticating user.
    :returns: `True` if the user authenticated successfully, `False` if there are credential errors.
    """
    user_string = f"cn={username},ou=Users,{os.environ['LDAP_BASE_DN']}"
    TLS = Tls(
        local_certificate_file=Path(os.environ["FASTAPI_LDAP_CERTS"])
        / f"{os.environ['FASTAPI_LDAP_CERT_NAME']}.crt",
        local_private_key_file=Path(os.environ["FASTAPI_LDAP_CERTS"])
        / f"{os.environ['FASTAPI_LDAP_CERT_NAME']}.key",
    )
    try:
        server = Server(
            os.environ["LDAP_HOST"], port=636, use_ssl=True, get_info="ALL", tls=TLS
        )
        connection = Connection(
            server, user=user_string, password=password, raise_exceptions=False
        )
    except _LDAPException as e:
        raise LDAPException(message=e.message)

    if connection.bind():
        return True

    failure_reason = connection.result["description"]
    if failure_reason == "invalidCredentials":
        return False

    raise LDAPException(message=failure_reason)
