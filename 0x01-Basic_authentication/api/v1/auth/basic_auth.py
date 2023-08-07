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

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads auth and retrieves the User instance for a request"""
        authorizationHeader = self.authorization_header(
            request)  # Get Authorization header
        if not authorizationHeader:
            return None

        b64Header = self.extract_base64_authorization_header(
            authorizationHeader)  # Extract the base64 toke
        if not b64Header:
            return None

        decodedHeader = self.decode_base64_authorization_header(
            b64Header)  # Decode the base64 token
        if not decodedHeader:
            return None

        # Extract user email and password from decoded token
        email, password = self.extract_user_credentials(decodedHeader)
        if not email or not password:
            return None

        user = self.user_object_from_credentials(
            email, password)  # Retrieve user object from storage
        if not user:
            return None

        return user
