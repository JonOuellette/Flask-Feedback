from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def connect_db(app):
    """Connects this database to the flask app"""
    db.app = app
    db.init_app(app)

class Users(db.Model):
    