#!/usr/bin/env python3
"""Basic authentication module"""

from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User
from models.base import Base


class BasicAuth(Auth):
    """Handles basic authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts and returns the base64 part of the Authorization header"""
        if not authorization_header or type(authorization_header) != str or\
                authorization_header.split()[0] != "Basic":
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Returns the decoded value of the base64_authorization_header"""
        if not base64_authorization_header or type(
                base64_authorization_header) != str:
            return None
        try:
            decoded = b64decode(base64_authorization_header)
            return str(decoded, "utf-8")
        except ValueError:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns the email and password from the base64 decoded value"""
        if not decoded_base64_authorization_header or type(
                decoded_base64_authorization_header) != str or ":"\
                not in decoded_base64_authorization_header:
            return (None, None)

        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """Returns a User instance based on email and password"""
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None

        user: User = User().search({"email": user_email})

        if not user or len(user) == 0:
            return None

        user = user[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user
