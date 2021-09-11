from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    VARBINARY,
    JSON,
    Enum)
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import relationship

# local imports
from todo_app.config.db_handler import handler
from sqlalchemy.sql import expression
from todo_app.models.common_models import DatetimeMixin


class TblUsers(DatetimeMixin, handler.Base):
    """
    SQL Alchemy Model for - Users
    """

    __tablename__ = "tbl_users"
    user_id = Column(
        Integer, nullable=False, primary_key=True, unique=True, autoincrement=True
    )
    firstname = Column(String(64), nullable=False)
    lastname = Column(String(64), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    phone = Column(String(256), nullable=False)
    password_hash = Column(VARBINARY(64))
    is_deleted = Column(Boolean, server_default=expression.false())

    def __repr__(self):
        return "<TblUsers %r>" % (self.email)

    def to_json(self):
        return {
            'mc_user_id': self.user_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone': self.phone,
        }
