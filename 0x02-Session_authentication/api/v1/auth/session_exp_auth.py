#!/usr/bin/env python3
"""Handles session expiration"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session expiration class"""

    def __init__(self):
        """Init method"""
        self.session_duration = getenv("SESSION_DURATION")
        try:
            self.session_duration = int(self.session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a session"""
        sessionID = super().create_session(user_id)
        if not sessionID:
            return None

        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        self.user_id_by_session_id[sessionID] = session_dictionary
        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """Returns user_id if user session hasn't expired"""
        if not session_id or not self.user_id_by_session_id[session_id]:
            return None

        user_id = self.user_id_by_session_id[session_id]['user_id']
        if int(self.session_duration) < 1:
            return user_id

        created_at = self.user_id_by_session_id[session_id].get("created_at")
        if not created_at:
            return None

        session_expiry = created_at + timedelta(seconds=self.session_duration)
        if session_expiry < datetime.now():
            return None

        return user_id
