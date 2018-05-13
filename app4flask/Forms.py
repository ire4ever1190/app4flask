from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('App4 Username', validators=[DataRequired()])
    password = PasswordField('App4 Password', validators=[DataRequired()])
    update = BooleanField('Update Timetable')
    submit = SubmitField('Sign In')