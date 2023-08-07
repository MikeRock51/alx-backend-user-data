#!/usr/bin/env python3
"""Basic authentication module"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Handles basic authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts and returns the base64 part of the Authorization header"""
        if not authorization_header or type(authorization_header) != str or\
                authorization_header.split()[0] != "Basic":
            return None
        return authorization_header.split()[1]
