#!/usr/bin/env python3
"""The auth module to handle authentication"""

from flask import request
from typing import List, TypeVar 


class Auth:
    """Manages the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns false...I guesss"""
        return False

    def authorization_header(self, request=None) -> str:
        """Iono yet..."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Still don't know"""
        return None
