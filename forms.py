"""forms for flask app"""

from wtforms import SearchField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm