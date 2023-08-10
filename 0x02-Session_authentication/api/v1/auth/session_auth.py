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

        sessionID = str(uuid4())
        self.user_id_by_session_id[sessionID] = user_id

        return sessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user ID based on session_id"""
        if not session_id or type(session_id) != str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a user based on the cookie value"""
        from models.user import User
        sessionID = self.session_cookie(request)
        if not sessionID:
            return None

        userID = self.user_id_for_session_id(sessionID)
        if not userID:
            return None

        user = User.get(userID)
        return user

    def destroy_session(self, request=None):
        """Deletes a users session"""
        if not request:
            return False
        sessionID = self.session_cookie(request)
        if not sessionID:
            return False

        userID = self.user_id_by_session_id[sessionID]
        if not userID:
            return False

        del self.user_id_by_session_id[sessionID]
        return True
