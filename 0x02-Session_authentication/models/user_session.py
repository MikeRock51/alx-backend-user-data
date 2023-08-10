#!/usr/bin/env python3
"""User Session module"""

from models.base import Base
from uuid import uuid4


class UserSession(Base):
    """User Session model"""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize an instance"""
        super().__init__(*args, **kwargs)
        self.user_id = None
