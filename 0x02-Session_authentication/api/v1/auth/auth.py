#!/usr/bin/env python3
"""The auth module to handle authentication"""

from flask import make_response
from typing import List, TypeVar
import re
from os import getenv


class Auth:
    """Manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks whether or a not a path requires authentication"""
        if not path or not excluded_paths or len(excluded_paths) < 1:
            return True

        if path[-1] != '/':
            path = path + '/'

        if path in excluded_paths:
            return False

        if any(re.match(pattern[:-1], path) for pattern in excluded_paths):
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header from request if any"""
        if request is None:
            return None

        authorization = request.headers.get('Authorization')

        return authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """Still don't know"""
        return None

    def session_cookie(self, request=None):
        """Returns the value of the session cookie"""
        if not request:
            return None

        cookieName = getenv("SESSION_NAME")
        sessionCookie = request.cookies.get(cookieName)

        return sessionCookie
