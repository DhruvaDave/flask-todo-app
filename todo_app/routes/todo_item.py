import logging
from flask import Blueprint, request

from todo_app.common.forms.todo_item_management_forms import \
    (TodoItemForm, AssignTodoItemForm, AddCommentTodoItemForm)
from todo_app.services.todo_item_management_service.todo_item_management_data\
    import TodoItemData
from todo_app.utils.session_management import have_logged_in


logger = logging.getLogger(__name__)

todo_item_management_process = Blueprint("todo_item_management_process", __name__)


@todo_item_management_process.route("", methods=["POST"])
@have_logged_in()
def add_todo_item():
    """
        Add Todo Item
    """
    logger.info('Incoming request for add todo item.')
    form = TodoItemForm()
    response = TodoItemData.todo_item_add(form)
    return response

@todo_item_management_process.route("/assign", methods=["POST"])
@have_logged_in()
def assign_todo_item():
    """
        Assign Todo Item
    """
    logger.info('Incoming request for assign todo item.')
    form = AssignTodoItemForm()
    response = TodoItemData.assign_todo_item(form)
    return response

@todo_item_management_process.route("/assign", methods=["GET"])
@have_logged_in()
def get_assign_todo_item():
    """
        Get Assign Todo Item assign to user
    """
    logger.info('Incoming request for get assign todo item to user.')
    query_params = request.args
    response = TodoItemData.get_assign_todo_item(query_params)
    return response


@todo_item_management_process.route("/comment", methods=["POST"])
@have_logged_in()
def post_comment_todo_item():
    """
        Add Comment Todo Item
    """
    logger.info('Incoming request for add comment todo item.')
    form = AddCommentTodoItemForm()
    response = TodoItemData.add_comment_todo_item(form)
    return response