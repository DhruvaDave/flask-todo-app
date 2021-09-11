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
from todo_app.models.todo_list import TblTodoLists


class TblUserTodoList(DatetimeMixin, handler.Base):
    """
    SQL Alchemy Model for - User Todo List 
    """

    __tablename__ = "tbl_user_todo_list"
    user_todo_list_id = Column(
        Integer, nullable=False, primary_key=True, unique=True, autoincrement=True
    )
    user_id_fk = Column(Integer, ForeignKey("tbl_users.user_id"))
    todo_list_id_fk = Column(Integer, ForeignKey("tbl_todo_lists.todo_list_id"))
    name = Column(String(140), nullable=True)


    def __repr__(self):
        return "<TblUserTodoList %r>" % (self.follwer_id)

    def to_json(self):
        return {
            'user_todo_list_id': self.user_todo_list_id,
            'user_id_fk': self.user_id_fk,
            'todo_list_id_fk': self.todo_list_id_fk
        }
