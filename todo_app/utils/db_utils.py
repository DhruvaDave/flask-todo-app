"""
    Database Utils
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(level=logging.INFO)


class MySQLHandler:
    """
    MySQL handler for db query
    """

    def __init__(
        self,
        host,
        user,
        password,
        port,
        dbname="",
        pool_size=5,
    ):
        self.host = host
        self.__user = user
        self.__password = password
        self.port = int(port)
        self.dbname = dbname
        self.pool_size = int(pool_size)
        self.url = None
        self._validate_credentials()
        self._create_engine()

    def _validate_credentials(self):
        if self.host is None:
            raise Exception("No host specified for MySQL")
        if self.__user is None:
            raise Exception("No user specified for MySQL")
        if self.__password is None:
            raise Exception("No password specified for MySQL")
        if self.dbname is None or self.dbname == "":
            raise Exception("No db specified for MySQL")

    def _get_connection_string(self):
        self.url = (
            "mysql+pymysql://"
            + self.__user
            + ":"
            + self.__password
            + "@"
            + self.host
            + ":"
            + str(self.port)
            + "/"
            + self.dbname
        )

    def _create_engine(self):
        self._get_connection_string()

        self.engine = create_engine(
            self.url, pool_size=self.pool_size, pool_pre_ping=True, pool_recycle=300, echo=False,
            isolation_level="READ UNCOMMITTED")
        self.db_session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
        # pylint: disable=C0103
        # note: Ignoring C0103: Attribute name as it's a modeling class
        self.Base = declarative_base(bind=self.engine)
        self.Base.query = self.db_session.query_property()

    def initialize_db(self):
        """
        Create db if not exists
        """
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        else:
            # Connect the database if exists.
            self.engine.connect()
