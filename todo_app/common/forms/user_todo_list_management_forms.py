import logging
import wtforms_json

from flask_wtf import Form
from wtforms.validators import DataRequired, Optional
from wtforms import StringField, FormField, FieldList, IntegerField


logger = logging.getLogger(__name__)

wtforms_json.init()


class UserTodoListForm(Form):
    name = StringField(validators=[DataRequired()])
