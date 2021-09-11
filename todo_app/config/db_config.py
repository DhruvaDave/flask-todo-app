"""
    Config related to db
"""
from os import environ
import logging

logger = logging.getLogger("DB-Config")


class DBConfig:
    """
    Database configuration
    """

    host = environ.get("DB_HOST")
    port = environ.get("DB_PORT", 3306)
    user = environ.get("DB_USER")
    password = environ.get("DB_PASSWORD")
    charset = environ.get("DB_CHARSET", "utf8")
    dbname = environ.get("DB_NAME")
    pool_size = environ.get("DB_POOLSIZE", 5)

    if host is None:
        logger.info(f"Database Host is not found")
    if user is None:
        logger.info(f"Database User is not found")
    if password is None:
        logger.info(f"Database Password is not found")
