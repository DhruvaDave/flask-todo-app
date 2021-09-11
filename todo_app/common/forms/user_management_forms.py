import logging
import wtforms_json

from flask_wtf import Form
from wtforms.validators import DataRequired, Optional
from wtforms import StringField, FormField, FieldList

from todo_app.common.validators.custom_validators import PasswordValidator
from .common_forms import EmailForm

logger = logging.getLogger(__name__)

wtforms_json.init()


class SignupForm(EmailForm):
    firstname = StringField(validators=[DataRequired()])
    lastname = StringField(validators=[DataRequired()])
    phone = StringField(validators=[DataRequired()])
    password = StringField(validators=[DataRequired(), PasswordValidator()])


class LoginForm(EmailForm):
    password = StringField(validators=[DataRequired()])
