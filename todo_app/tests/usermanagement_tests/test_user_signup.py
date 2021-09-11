import unittest
import unittest.mock as mock

from flask import Flask
from datetime import datetime
from werkzeug.datastructures import MultiDict
import datetime

from todo_app.common import constants
from todo_app.exceptions.http_exception import HttpException
from todo_app.models.user_management import TblUsers


from todo_app.common.forms.user_management_forms import (
    SignupForm,
    LoginForm,
)
from todo_app.services.user_management_service.user_management_data import (
    UsersData,
)

mock_create_user = "todo_app.services.user_management_service.user_management_data.UserRepo.create_users"
mock_fetch_user_by_email = "todo_app.services.user_management_service.user_management_data.UserRepo.fetch_user_by_email"

class TestUser(unittest.TestCase):
    '''
    Class for user tests on Verify MFA API
    '''
    def setUp(self):
        self.app = app = Flask(__name__)
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        self.signup_data={
            "firstname": "elon",
            "lastname": "muskhere",
            "phone": "9876543210",
            "email": "elonmuskhere@gmail.com",
            "password": "Cytrio@123"
        }
        self.signup_form = SignupForm(MultiDict(self.signup_data))
        self.signup_fail_data={
            "firstname": "elon",
            "lastname": "muskhere",
            "email": "elonmuskhere@gmail.com",
            "phone": "9876543210"
        }
        self.signup_fail_form = SignupForm(MultiDict(self.signup_fail_data))
        self.no_user_data={}
        
        self.table_users_data = {'email': 'elonmuskhere@gmail.com', 'phone': '9876543210',
                               'created_at': datetime.datetime(2021, 5, 24, 15, 42, 1),
                               'password_hash': b'4a8cce82b9699f6425c570ca704f17a3c968bb44',
                               'updated_at': datetime.datetime(2021, 5, 24, 15, 42, 57),
                               'user_id': 28,
                               'firstname': 'Elon', 'lastname': 'Musk'}
        self.table_users = TblUsers(**self.table_users_data)

    def test_signup_failure(self):
        """
        Unit test for failure case of update_by method
        """
        with self.app_context:
            with mock.patch(mock_create_user, return_value= 0):
                with mock.patch("todo_app.common.forms.user_management_forms.SignupForm.is_submitted",
                                return_value=True):
                    try:
                        response = UsersData.user_sign_up(self.signup_fail_form)
                    except HttpException as e:
                        assert e.code == constants.BAD_REQUEST


    def test_signup_success(self):
        """
        Unit test for success case of MC User Sign Up
        """
        with self.app_context:
            with mock.patch(mock_create_user, return_value=self.table_users.user_id):
                with mock.patch(mock_fetch_user_by_email, return_value=False):
                    with mock.patch("todo_app.common.forms.user_management_forms.SignupForm.is_submitted",
                                    return_value=True):
                        response = UsersData.user_sign_up(self.signup_form)
                        assert response.status_code == 200

if __name__ == "__main__":
    unittest.main()
