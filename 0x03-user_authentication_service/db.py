"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
# import from .exc
from sqlalchemy.exc import InvalidRequestError
from user import Base, User
from typing import Dict

UserFields = ['id', 'email', 'session_id', 'hashed_password', 'reset_token']


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Saves a user to the database"""
        if not email or not hashed_password:
            return None

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs: Dict) -> User:
        """Returns the first row with the provided key, word argument"""
        if not kwargs or any(key not in UserFields for key in kwargs):
            raise InvalidRequestError

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound as e:
            raise e

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """Updates the user with the user_id"""
        user = self.find_user_by(id=user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if key not in UserFields:
                raise ValueError
            setattr(user, key, value)

        self._session.commit()
