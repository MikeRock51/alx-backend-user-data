#!/usr/bin/env python3
"""Session Authentication Module"""

from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Handles session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for the user_id"""
        if not user_id or type(user_id) != str:
            return None

        sessionID = uuid4()
        self.user_id_by_session_id[str(sessionID)] = user_id

        return sessionID
