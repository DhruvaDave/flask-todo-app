from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email


# Base forms
class EmailForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
