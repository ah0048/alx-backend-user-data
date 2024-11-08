#!/usr/bin/env python3
'''function called filter_datum that returns the log message obfuscated'''
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
        '''function called format that returns the log message obfuscated'''
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''function called filter_datum that returns the log message obfuscated'''
    for field in fields:
        message = re.sub(rf'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    '''function called get_logger that returns a logging.Logger object'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connection to MySQL environment """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    try:
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
        return connection
    except mysql.connector.Error as err:
        raise err


def main():
    '''
    function called main that will obtain a
    database connection using get_db
    '''
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        logger.info(f"name={row[0]}; phone={row[1]}; email={row[2]}; \
                    ssn={row[3]}; password={row[4]}; ip={row[5]}; \
                        last_login={row[6]};")
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
