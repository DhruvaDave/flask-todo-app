import logging
from flask import Blueprint

from todo_app.common.forms.user_management_forms import (
    SignupForm,
    LoginForm,
)
from todo_app.services.user_management_service.user_management_data import (
    UsersData,
)

logger = logging.getLogger(__name__)

user_management_process = Blueprint("user_management_process", __name__)


@user_management_process.route("/signup", methods=["POST"])
def signup():
    """
        Signup
    """
    logger.info('Incoming request for user signup.')
    form = SignupForm()
    response = UsersData.user_sign_up(form)
    return response


@user_management_process.route("/login", methods=["POST"])
def login():
    """
        Login
    """
    logger.info('Incoming request for user login.')
    form = LoginForm()
    response = UsersData.user_login(form)
    return response

