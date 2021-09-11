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


class TblTodoLists(DatetimeMixin, handler.Base):
    """
    SQL Alchemy Model for - Todo Lists
    """

    __tablename__ = "tbl_todo_lists"
    todo_list_id = Column(
        Integer, nullable=False, primary_key=True, unique=True, autoincrement=True
    )
    name = Column(String(140), nullable=False)


    def __repr__(self):
        return "<TblTodoLists %r>" % (self.name)

    def to_json(self):
        return {
            'todo_list_id': self.todo_list_id,
            'name': self.name
        }
