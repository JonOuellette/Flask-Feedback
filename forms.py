"""forms for flask app"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class LoginForm(FlaskForm):
    """User login form"""

    username = StringField("Username", validators = [InputRequired(), Length(min=1, max=25)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max =20)])

class RegisterForm(FlaskForm):

    username = StringField("Username", validators = [InputRequired(), Length(min=1, max=25)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max =20)])
    email = StringField("Email", validators= [InputRequired(), Email(),])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])


class FeedbackForm(FlaskForm):
    """User Feedback Form"""
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])