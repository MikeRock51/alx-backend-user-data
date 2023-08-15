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

UserFields = ['id', 'email', 'session_id' 'hashed_password', 'reset_token']


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        if not email or type(email) != str:
            return None
        if not hashed_password or type(hashed_password) != str:
            return None

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """Returns the first row with the provided key, word argument"""
        if not kwargs or any(key not in UserFields for key in kwargs):
            raise InvalidRequestError

        session = self._session

        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound as e:
            raise e
