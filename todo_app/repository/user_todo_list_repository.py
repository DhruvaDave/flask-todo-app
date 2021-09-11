import logging

from sqlalchemy import desc
from todo_app.config.db_handler import handler

from todo_app.models.user_todo_list import TblUserTodoList

logger = logging.getLogger(__name__)

db_session = handler.db_session


class UserTodoListRepo:

    @staticmethod
    def create_user_todo_list(todo_list_data):
        """
        Create Todo list
        """

        db_session.add(TblUserTodoList(**todo_list_data))
        db_session.flush()
        db_session.commit()

        return True
        