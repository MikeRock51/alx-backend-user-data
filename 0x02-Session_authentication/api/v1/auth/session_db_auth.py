#!/usr/bin/env python3
"""DB Session authentication module"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Manages user sessions from db"""
    def create_session(self, user_id=None):
        """Creates and stores a new User Session"""
        if not user_id or type(user_id) != str:
            return None
        session = UserSession()
        session.user_id = user_id
        session.save()

        return session.id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user_id based on the session_id"""
        if not session_id or type(session_id) != str:
            return None

        session: UserSession = UserSession().get(session_id)
        if not session:
            return None

        session_expiry = session.created_at + \
            timedelta(seconds=self.session_duration)
        if session_expiry < datetime.utcnow():
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """Deletes the UserSession instance based on session ID"""
        if not request:
            return False

        sessionID = self.session_cookie(request)
        if not sessionID:
            return False

        session: UserSession = UserSession.get(sessionID)
        if not sessionID:
            return False

        session.remove()
        return True
