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
from registration_app.orm.models import UserInfoCreate

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


def establish_ldap_connection(user_dn: str, password: str) -> Connection:
    """
    Establish a connection to the OpenLDAP backend.

    :param user_dn: The distinguished name of the user.
    :param password: The password to use in th connection.
    :raises _LDAPException: If there is any exception in creating the server or connection. Note
    that `Connection.result` should still be checked for exceptions.
    :return: The established connection.
    """
    TLS = Tls(
        local_certificate_file=Path(os.environ["FASTAPI_LDAP_CERTS"])
        / f"{os.environ['FASTAPI_LDAP_CERT_NAME']}.crt",
        local_private_key_file=Path(os.environ["FASTAPI_LDAP_CERTS"])
        / f"{os.environ['FASTAPI_LDAP_CERT_NAME']}.key",
    )
    server = Server(
        os.environ["LDAP_HOST"], port=636, use_ssl=True, get_info="ALL", tls=TLS
    )
    return Connection(server, user=user_dn, password=password, raise_exceptions=False)


def user_authenticate(username: str, password: str) -> bool:
    """
    Authenticate user against LDAP.

    :param username: The username of the user attempting to authenticate.
    :param password: The password of the authenticating user.
    :raises LDAPException: If there is an issue establishing the ldap connection (or other
        unexpected errors.)
    :returns: `True` if the user authenticated successfully, `False` if there are credential errors.
    """
    try:
        connection = establish_ldap_connection(
            user_dn=f"cn=admin,{os.environ['LDAP_BASE_DN']}",
            password=os.environ["LDAP_ADMIN_PASSWORD"],
        )
    except _LDAPException as e:
        raise LDAPException(message=e.message)

    if not connection.bind():
        raise LDAPException(
            message="There was an issue with registration. "
            "Please contact the administrator if the issue continues."
        )

    auth_or_no = connection.search(
        search_base={os.environ["LDAP_BASE_DN"]},
        search_filter=f"(&(|(cn={username})(mail={username}))(userpassword={password}))",
    )

    if connection.result["description"] == "success":
        connection.unbind()
        return auth_or_no
    else:
        raise LDAPException(message=connection.result["description"])


def create_user_in_ldap(user: UserInfoCreate) -> tuple[bool, str]:
    """
    Create a user in LDAP.

    :param user: The user to create.
    :raises LDAPException: If there is an issue establishing the ldap connection (or other
        unexpected errors.)
    :return: True if the user was created, False with the reason for lack of creation otherwise.
    """
    try:
        connection = establish_ldap_connection(
            user_dn=f"cn=admin,{os.environ['LDAP_BASE_DN']}",
            password=os.environ["LDAP_ADMIN_PASSWORD"],
        )
    except _LDAPException as e:
        raise LDAPException(message=e.message)

    if not connection.bind():
        raise LDAPException(
            message="There was an issue with registration. "
            "Please contact the administrator if the issue continues."
        )
    registered_email = connection.search(
        search_base={os.environ["LDAP_BASE_DN"]},
        search_filter=f"(mail={user.email})",
    )

    if registered_email:
        return (False, "email")

    connection.add(
        f"cn={user.username},ou=Users,{os.environ['LDAP_BASE_DN']}",
        ["inetOrgPerson", "top"],
        {
            "sn": user.last,
            "mail": user.email,
            "userpassword": user.password.get_secret_value(),
        },
    )
    result = connection.result
    connection.unbind()
    if result["result"]:
        if result["description"] == "entryAlreadyExists":
            return (False, "username")
        else:
            raise LDAPException(message=result["description"])
    return (True, "")
