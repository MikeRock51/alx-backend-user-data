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
                 message: str, seperator: str) -> str:
    """Uses regex to replace occuerences of certain values"""
    for field in fields:
        message = re.sub(f"{field}=([^{seperator}]+)",
                         f"{field}={redaction}", message)
    return message
