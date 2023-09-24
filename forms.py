"""forms for flask app"""
from flask_wtf import FlaskForm
from wtforms import SearchField, PasswordField
from wtforms.validators import InputRequired, Length, Email
