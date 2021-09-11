import json
import logging

from flask import jsonify

from todo_app.common import constants
from todo_app.exceptions.http_exception import HttpException

from todo_app.repository.user_todo_list_repository import UserTodoListRepo

from todo_app.common import messages
from todo_app.utils.session_management import get_current_user_id
from todo_app.utils.pagination import get_pagination
from todo_app.utils.http_response_handler import HttpResponseHandler

logger = logging.getLogger(__name__)


class UserTodoListData:

    @staticmethod
    def create_user_todo_list(form):
        if not form.validate_on_submit():
            logging.debug(messages.INVALID_FORM_MESSAGE, form.errors)
            raise HttpException(messages.INVALID_FORM_MESSAGE,
                                constants.BAD_REQUEST, 400)
              
        data = {
            "user_id_fk": get_current_user_id(),
            "name": form.name.data,
        }
        UserTodoListRepo.create_user_todo_list(data)
       
        return jsonify(
            {
                "code": constants.CREATED,
                "message": "Todo List Created Successfully"
            }
        ),  constants.ENTITY_CREATED

    
  