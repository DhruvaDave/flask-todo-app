# pylint: disable=W0621
# W0621: Redefining name from outer scope

import logging
from flask import session
from todo_app.common.constants import UNAUTHORISED
from todo_app.exceptions.http_exception import HttpException
from todo_app.utils.jwt_encipherment import decode_jwt_token
from todo_app.common import constants

logger = logging.getLogger(__name__)


def create_session(jwt_token):
    """
    Storing session data
    """
    session["jwt_token"] = jwt_token


def get_session_data(session):
    """
    Extracting Session data from JWT payload
    """
    if "jwt_token" not in session.keys():
        raise HttpException(code=UNAUTHORISED, http_code=401, message="User Not Logged In")
    jwt_token = session["jwt_token"]
    data = decode_jwt_token(jwt_token)
    return data

def get_current_user_id():
    session_data = get_session_data(session)
    user_id = session_data["jwt_payload"]["user_id"]
    return user_id

def have_logged_in():
    def decorator(api_route):
        def wrapper(*args, **kwargs):
            if session:
                return api_route(*args, **kwargs)
            return {"code": constants.FORBIDDEN, "message": "Please login."}, 403
        wrapper.__name__ = api_route.__name__
        return wrapper
    return decorator