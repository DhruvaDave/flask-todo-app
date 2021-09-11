import logging
import wtforms_json

from flask_wtf import Form
from wtforms.validators import DataRequired
from wtforms import IntegerField, StringField, FieldList, Field

logger = logging.getLogger(__name__)

wtforms_json.init()

class ListField(Field):
    def process_formdata(self, valuelist):
        self.data = valuelist

class TodoItemForm(Form):
    todo_list_id = IntegerField()
    user_todo_list_id = IntegerField()
    title = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])
    start_date = StringField()
    due_date = StringField()
    status = StringField(validators=[DataRequired()])
    parent_todo_item_id = IntegerField()
    assign_to = ListField()
    comment = StringField()



class AssignTodoItemForm(Form):
    todo_item_id = IntegerField(validators=[DataRequired()])
    assign_to = ListField([DataRequired()])


class AddCommentTodoItemForm(Form):
    todo_item_id = IntegerField(validators=[DataRequired()])
    comment = StringField([DataRequired()])