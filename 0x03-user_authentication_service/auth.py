#!/usr/bin/env python3
"""Authentication module"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns it"""
    hashed_password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """Generates and returns a uuid string"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Creates a new user and saves to database"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            savedPwd = user.hashed_password
            credPwd = password.encode('UTF-8')

            if bcrypt.checkpw(credPwd, savedPwd):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session id for the email user"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retireves the user with the session_id"""
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session"""
        if not user_id:
            return None

        try:
            user = find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            return
