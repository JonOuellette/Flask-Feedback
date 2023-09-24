"""forms for flask app"""
from flask_wtf import FlaskForm
from wtforms import Stringfield, PasswordField
from wtforms.validators import InputRequired, Length, Email

class LoginForm(FlaskForm):
    """User login form"""

    username = Stringfield("Username", validators = [InputRequired(), Length(min=1, max=25)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max =20)])

class RegisterForm(FlaskForm):

    username = Stringfield("Username", validators = [InputRequired(), Length(min=1, max=25)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max =20)])
    email = Stringfield("Email", validators= [InputRequired(), Email(),])
    first_name = Stringfield("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = Stringfield("Last Name", validators=[InputRequired(), Length(max=30)])