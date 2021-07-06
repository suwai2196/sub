import json

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError


class RegisterForm(FlaskForm):
    teacherName = StringField(label='Name', validators=[Length(min=2, max= 30, message='Name must be between 2 and 30 characters long.'), DataRequired()])
    teacherId = StringField(label='ID', validators=[Length(min=6, message='Id must be at least 5 characters long.'), DataRequired()])
    submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
    teacherId = StringField(label="ID", validators=[DataRequired()])
    submit = SubmitField(label="Log In")
