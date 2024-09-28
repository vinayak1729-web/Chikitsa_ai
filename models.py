from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, gensalt, checkpw

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))