from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt()
db=SQLAlchemy()

def connect_db(app):
    """Connects this database to the flask app"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Sites user"""

    __tablename__ = "users"

    username = db.Column(db.String, primary_key = True, unique = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String, nullable = False)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """registers user with a hashed password and returns user"""
        
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)   

        return user 
    
    @classmethod
    def authenticate(cls, username, password,):
        """Validates that the user exists and that the password is correct.  
        Returns user if valid if not returns false"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            
            return user
        else: 
            return False