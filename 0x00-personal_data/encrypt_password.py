#!/usr/bin/env python3
"""Handles user password"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a hashed version of the given password"""
    hashed = bcrypt.hashpw(bytes(password, "UTF-8"), bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if given password matches the hashed password"""
    return bcrypt.checkpw(bytes(password, "UTF-8"), hashed_password)
