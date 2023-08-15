#!/usr/bin/env python3
"""Authentication module"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns it"""
    hashed_password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
    return hashed_password
