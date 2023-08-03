#!/usr/bin/env python3
"""
    Write a function called filter_datum that
    returns the log message obfuscated:

    Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is
        separating all fields in the log line (message)
        The function should use a regex to replace
        occurrences of certain field values.
        filter_datum should be less than 5 lines long and use
        re.sub to perform the substitution with a single regex.
"""

import logging
import re
from typing import List
from mysql.connector.connection_cext import CMySQLConnection
import mysql.connector
from os import getenv


PII_FIELDS = ("email", "ssn", "password", "phone", "name")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Applies redaction to incoming records"""
        msg = filter_datum(self.fields, self.REDACTION, record.msg,
                           self.SEPARATOR)
        record.msg = msg
        message = super().format(record)

        return message


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Uses regex to replace occurrences of certain values"""
    for field in fields:
        message = re.sub(f"{field}=([^{separator}]+)",
                         f"{field}={redaction}", message)
    return message


def get_logger() -> logging.Logger:
    """Handles user_data logging"""
    logger = logging.getLogger("user_data")
    streamHandler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    return logger


def get_db() -> CMySQLConnection:
    """Returns a connector to the requested datbase"""
    config = {
        "user": getenv("PERSONAL_DATA_DB_USERNAME") or "root",
        "password": getenv("PERSONAL_DATA_DB_PASSWORD") or "",
        "host": getenv("PERSONAL_DATA_DB_HOST") or "localhost",
        "database": getenv("PERSONAL_DATA_DB_NAME")
    }

    connector = mysql.connector.connect(**config)

    return connector
