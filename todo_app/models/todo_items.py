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
from todo_app.models.user_todo_list import TblUserTodoList

class TblTodoItems(DatetimeMixin, handler.Base):
    """
    SQL Alchemy Model for - Todo List owner
    """

    __tablename__ = "tbl_todo_items"
    todo_item_id = Column(
        Integer, nullable=False, primary_key=True, unique=True, autoincrement=True
    )
    todo_list_id_fk = Column(Integer, ForeignKey("tbl_todo_lists.todo_list_id"))
    user_todo_list_id_fk = Column(Integer, ForeignKey("tbl_user_todo_list.user_todo_list_id"))
    parent_todo_item_id_fk = Column(Integer, ForeignKey("tbl_todo_items.todo_item_id"))
    user_id_fk = Column(Integer, ForeignKey("tbl_users.user_id"))
    title = Column(String(140), nullable=True)
    description = Column(String(140), nullable=True)
    start_date = Column(TIMESTAMP, nullable=True)
    due_date = Column(TIMESTAMP, nullable=True)
    status = Column(String(140)) 
    comment = Column(String(1024)) 


    def __repr__(self):
        return "<TblTodoItems %r>" % (self.todo_item_id)

    def to_json(self):
        return {
            'todo_item_id': self.todo_item_id,
            'user_todo_list_id_fk': self.user_todo_list_id_fk,
            'parent_todo_item_id_fk': self.parent_todo_item_id_fk,
            'title': self.title,
            'description': self.description,
            'status': self.status
        }


class TblTodoItemUsers(DatetimeMixin, handler.Base):
    """
    SQL Alchemy Model for - Todo Item Users
    """

    __tablename__ = "tbl_todo_item_users"
    todo_item_user_id = Column(
        Integer, nullable=False, primary_key=True, unique=True, autoincrement=True
    )
    todo_item_id_fk = Column(Integer, ForeignKey("tbl_todo_items.todo_item_id"))
    assigned_user_id_fk = Column(Integer, ForeignKey("tbl_users.user_id"))

    def __repr__(self):
        return "<TblTodoItemUsers %r>" % (self.todo_item_user_id)
