import json
import logging
from flask import session, jsonify

from todo_app.common import constants
from todo_app.exceptions.http_exception import HttpException

from todo_app.repository.user_repository import UserRepo

from todo_app.utils.password_enc import generate_password_hash
from todo_app.common import messages

from todo_app.config.app_config import CommonConfig
from todo_app.repository.user_repository import UserRepo
from todo_app.utils.jwt_encipherment import generate_jwt_token
from todo_app.utils.http_response_handler import HttpResponseHandler
from todo_app.utils.session_management import create_session

logger = logging.getLogger(__name__)


class UsersData:

    @staticmethod
    def user_sign_up(form):
        if not form.validate_on_submit():
            logging.debug(messages.INVALID_FORM_MESSAGE, form.errors)
            response_dict = {
                'code': constants.BAD_REQUEST,
                'message': form.errors
            }
            return jsonify(response_dict), 400
            

        user_data = UserRepo.fetch_user_by_email(email=form.email.data)
        if user_data:
            logging.debug(f'User already exists with email {form.email.data}')
            return jsonify(
            {
                "code": constants.CREATED,
                "message": "User with this email is already created."
            }
        )
        
        data = {
            "firstname": form.firstname.data,
            "lastname": form.lastname.data,
            "phone": form.phone.data,
            "email": form.email.data,
            "password_hash": generate_password_hash(form.password.data).encode(
                "utf-8"
            )
        }
        user_id = UserRepo.create_users(data)

        return jsonify(
            {
                "code": constants.SUCCESS,
                "message": messages.SIGNUP_COMPLETED
            }
        )

    @staticmethod
    def user_login(form):
        """
        Login API Service Method
        """
        if not form.validate_on_submit():
            response_dict = {
                'code': constants.BAD_REQUEST,
                'message': form.errors
            }
            return jsonify(response_dict), 400
            
        email = form.email.data
        entered_password = form.password.data
        user_data = UserRepo.fetch_user_by_email(email=email)
        
        if not user_data:
            logging.debug(f"No User Exists for Email:{email} ")
            return HttpResponseHandler.invalid_credentials()
        
        entered_password_hash = generate_password_hash(
            entered_password).encode(constants.UTF_ENCODING)
        
        if entered_password_hash != user_data.password_hash:
            logging.debug(f"Invalid Password for email:{email}")
            return HttpResponseHandler.invalid_credentials()
        
        jwt_payload = {
                    "email": user_data.email,
                    "firstname": user_data.firstname,
                    "lastname": user_data.lastname,
                    "phone": user_data.phone,
                    "user_id": user_data.user_id
                }
        jwt_token = generate_jwt_token(user_data.email,
                                        CommonConfig.JWT_EXP_TIME_MINS, jwt_payload=jwt_payload)
        
        create_session(jwt_token)
        logging.debug('Session created for user')
        response_payload = {
            "jwt_token": {
                "token": jwt_token.decode("utf-8"),
                "exp_time_in_minutes": CommonConfig.
                    JWT_EXP_TIME_MINS,
            }
        }
        return HttpResponseHandler.success(message="User Logged In", **response_payload)

   