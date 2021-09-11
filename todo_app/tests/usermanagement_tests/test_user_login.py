"""
    Unit testing
"""
import unittest
import unittest.mock as mock
from flask import Flask
from datetime import datetime
import datetime

from werkzeug.datastructures import MultiDict
from todo_app.utils.jwt_encipherment import generate_jwt_token
from todo_app.models.user_management import TblUsers
from todo_app.exceptions.http_exception import HttpException
from todo_app.common import constants


from todo_app.common.forms.user_management_forms import (
    LoginForm,
)
from todo_app.services.user_management_service.user_management_data import (
    UsersData,
)

#mockpath
fetch_user_by_email_mockpath = "todo_app.services.user_management_service.user_management_data.UserRepo.fetch_user_by_email"
mock_create_session = "todo_app.services.user_management_service.user_management_data.create_session"


class TestLogin(unittest.TestCase):
    """
    Class for unit testing
    """
    def setUp(self):
        self.app = app = Flask(__name__)
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        self.form_data = {
            "email": "elonmuskhere@gmail.com",
            "password": "Cytrio@1234"
        }

        self.invalid_form_data = {
            "email": "elonmuskhere@gmail.com",
            "password": "Cytrio123"
        }

        self.incorrect_data = {
            "email": "elonmuskhere@gmail.com"
        }

        self.table_users_data = {'email': 'elonmuskhere@gmail.com', 'phone': '9876543210',
                               'created_at': datetime.datetime(2021, 5, 24, 15, 42, 1),
                               'password_hash': b'66877f59cc8ea99e9e782e4177b1b820180b9bfc9f9be113d8f06e365e4d66e7',
                               'updated_at': datetime.datetime(2021, 5, 24, 15, 42, 57),
                               'user_id': 28,
                               'firstname': 'Elon', 'lastname': 'Musk'}
        self.table_users = TblUsers(**self.table_users_data)

        self.no_form_data = {}
        self.login_form = LoginForm(MultiDict(self.form_data))
        self.no_form_data_login_form = LoginForm(MultiDict(self.no_form_data))
        self.invalid_form = LoginForm(MultiDict(self.invalid_form_data))
        self.incorrect_form = LoginForm(MultiDict(self.incorrect_data))
        self.jwt = generate_jwt_token(email="elonmuskhere@gmail.com", exp_time=10)
        self.form_submitted = "todo_app.common.forms.user_management_forms.LoginForm.is_submitted"

    def test_success_login(self):
        """
        Unit testing for success login
        """
        with self.app_context:
            with mock.patch(fetch_user_by_email_mockpath, return_value=self.table_users):
                with mock.patch(self.form_submitted,return_value=True):
                    with mock.patch(mock_create_session):
                        response, code = UsersData.user_login(self.login_form)
                        assert code == 200


    def test_invalid_login_data(self):
        """
        Unit testing for invalid login form data
        """
        with self.app_context:
            try:
                with mock.patch(self.form_submitted,
                                return_value=True):
                    response,code = UsersData.user_login(self.incorrect_form)
            except HttpException as e:
                assert e.code == constants.BAD_REQUEST

    def test_user_doesnot_exists(self):
        """
        Unit testing for User does not exists
        """
        with self.app_context:
            with mock.patch(fetch_user_by_email_mockpath, return_value=None):
                with mock.patch(self.form_submitted, return_value=True):
                    response,code = UsersData.user_login(self.login_form)
                    assert code == 400

    def test_password_mismatch(self):
        """
        Unit testing for Password mismatch
        """
        with self.app_context:
            with mock.patch(fetch_user_by_email_mockpath, return_value=self.table_users):
                with mock.patch(self.form_submitted, return_value=True):
                    response,code = UsersData.user_login(self.invalid_form)
                    assert code == 400


if __name__ == "__main__":
    unittest.main()