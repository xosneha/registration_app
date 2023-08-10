"""Module defining application-wide exceptions."""
# TODO Clean up poetry


class LDAPException(Exception):
    """Exceptions that may occur when interacting with LDAP."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
