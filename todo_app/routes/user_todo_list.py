import logging
from flask import Blueprint, request

from todo_app.common.forms.user_todo_list_management_forms import UserTodoListForm


from todo_app.services.user_todo_list_management_service.\
    user_todo_list_management_data import UserTodoListData
from todo_app.utils.session_management import have_logged_in

logger = logging.getLogger(__name__)

todo_list_management_process = Blueprint("todo_list_management_process", __name__)


@todo_list_management_process.route("", methods=["POST"])
@have_logged_in()
def add_todo_list():
    """
        Todo List
    """
    logger.info('Incoming request for add todo list.')
    form = UserTodoListForm()
    response = UserTodoListData.create_user_todo_list(form)
    return response



