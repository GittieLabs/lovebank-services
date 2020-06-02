from lovebank_services import db     # imports db variable from __init__.py

# User Model
class User(db.Model):
    ''' Define User model '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# Task Model
class Task(db.Model):
    ''' Define Task model '''
    id = db.Column(db.Integer, primary_key=True)
