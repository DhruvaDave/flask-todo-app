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


from todo_app.common.forms.todo_item_management_forms import TodoItemForm
from todo_app.services.todo_item_management_service.\
    todo_item_management_data import TodoItemData

#mockpath
get_current_user_mockpath = "todo_app.services.todo_item_management_service.todo_item_management_data.get_current_user_id"
create_todo_item_mockpath = "todo_app.services.todo_item_management_service.todo_item_management_data.TodoItemRepo.create_todo_item"
fetch_todo_item_mockpath = "todo_app.services.todo_item_management_service.todo_item_management_data.TodoItemRepo.fetch_user_todo_item"

class TestTododItem(unittest.TestCase):
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
            "title": "new list",
            "description": "New Todo item",
            "status": "todo" 
        }
        self.assign_form_data = {
            "title": "new list",
            "description": "New Todo item",
            "status": "todo" ,
            "assign_to": [1,2,3]
        }

        

        self.incorrect_form_data = {
            "title": "new list",
            "description": "New Todo item",
        }
        self.form = TodoItemForm(MultiDict(self.form_data))
        self.assign_form = TodoItemForm(MultiDict(self.assign_form_data))
        self.invalid_form = TodoItemForm(MultiDict(self.incorrect_form_data))

        self.form_submitted = "todo_app.common.forms.todo_item_management_forms.TodoItemForm.is_submitted"

    def test_success_create_item(self):
        """
        Unit testing for success create todo item
        """
        session_data = {'email': 'dhruva@gmail.com', 'exp': 1622016252,
                        'jwt_payload': {'email': 'dhruva@gmail.com', 'firstname': 'Dhruva', 
                        'lastname': 'Dave','phone': '9876543210', 'user_id': 1}}

        with self.app_context:
            with mock.patch(get_current_user_mockpath, return_value=session_data):
                with mock.patch(self.form_submitted,return_value=True):
                    with mock.patch(create_todo_item_mockpath, return_value=True):
                        response, code = TodoItemData.todo_item_add(self.form)
                        assert code == 200

    def test_success_create_item_with_assign(self):
        """
        Unit testing for success create todo item
        """
        session_data = {'email': 'dhruva@gmail.com', 'exp': 1622016252,
                        'jwt_payload': {'email': 'dhruva@gmail.com', 'firstname': 'Dhruva', 
                        'lastname': 'Dave','phone': '9876543210', 'user_id': 1}}

        with self.app_context:
            with mock.patch(get_current_user_mockpath, return_value=session_data):
                with mock.patch(self.form_submitted,return_value=True):
                    with mock.patch(create_todo_item_mockpath, return_value=True):
                        response, code = TodoItemData.todo_item_add(self.assign_form)
                        assert code == 200

    def test_invalid_item_data(self):
        """
        Unit testing for invalid todo item form data
        """
        with self.app_context:
            try:
                with mock.patch(self.form_submitted,
                                return_value=True):
                    response,code = TodoItemData.todo_item_add(self.invalid_form)
            except HttpException as e:
                assert e.code == constants.BAD_REQUEST

    # Here
    def test_success_get_item(self):
        """
        Unit testing for success get todo item
        """
        session_data = {'email': 'dhruva@gmail.com', 'exp': 1622016252,
                        'jwt_payload': {'email': 'dhruva@gmail.com', 'firstname': 'Dhruva', 
                        'lastname': 'Dave','phone': '9876543210', 'user_id': 1}}

        with self.app_context:
            with mock.patch(get_current_user_mockpath, return_value=session_data):
                with mock.patch(self.form_submitted,return_value=True):
                    with mock.patch(create_todo_item_mockpath, return_value=True):
                        response, code = TodoItemData.todo_item_add(self.form)
                        assert code == 200

if __name__ == "__main__":
    unittest.main()