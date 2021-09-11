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


from todo_app.common.forms.user_todo_list_management_forms import UserTodoListForm
from todo_app.services.user_todo_list_management_service.\
    user_todo_list_management_data import UserTodoListData

#mockpath
fetch_user_by_email_mockpath = "todo_app.services.user_management_service.user_management_data.UserRepo.fetch_user_by_email"
mock_create_session = "todo_app.services.user_management_service.user_management_data.create_session"
get_current_user_mockpath = "todo_app.services.user_todo_list_management_service.user_todo_list_management_data.get_current_user_id"
create_user_todo_list_mockpath = "todo_app.services.user_todo_list_management_service.user_todo_list_management_data.UserTodoListRepo.create_user_todo_list"

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
            "name": "new list",
        }

        self.list_form_data = {
            "list_id": 1
        }

        self.incorrect_form_data = {
            "temp": "abc"
        }
        self.form = UserTodoListForm(MultiDict(self.form_data))
        self.invalid_form = UserTodoListForm(MultiDict(self.incorrect_form_data))

        self.form_submitted = "todo_app.common.forms.user_todo_list_management_forms.UserTodoListForm.is_submitted"

    def test_success_create_list(self):
        """
        Unit testing for success create todo list
        """
        session_data = {'email': 'dhruva@gmail.com', 'exp': 1622016252,
                        'jwt_payload': {'email': 'dhruva@gmail.com', 'firstname': 'Dhruva', 
                        'lastname': 'Dave','phone': '9876543210', 'user_id': 1}}

        with self.app_context:
            with mock.patch(get_current_user_mockpath, return_value=session_data):
                with mock.patch(self.form_submitted,return_value=True):
                    with mock.patch(create_user_todo_list_mockpath, return_value=True):
                        response, code = UserTodoListData.create_user_todo_list(self.form)
                        assert code == 200


    def test_invalid_list_data(self):
        """
        Unit testing for invalid todo list form data
        """
        with self.app_context:
            try:
                with mock.patch(self.form_submitted,
                                return_value=True):
                    response,code = UserTodoListData.create_user_todo_list(self.invalid_form)
            except HttpException as e:
                assert e.code == constants.BAD_REQUEST

    # def test_user_not_logged_in(self):
    #     """
    #     Unit testing for User does not exists
    #     """
    #     with self.app_context:
    #         with mock.patch(get_current_user_mockpath, return_value=False):
    #             with mock.patch(self.form_submitted,return_value=True):
    #                 with mock.patch(create_user_todo_list_mockpath, return_value=False):
    #                     response, code = UserTodoListData.create_user_todo_list(self.form)
    #                     assert code == 400
                    # assert code == 400

    

if __name__ == "__main__":
    unittest.main()