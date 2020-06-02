from lovebank_services import db     # imports db variable from __init__.py
from datetime import datetime

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
    title = db.Column(db.String(50))
    description = db.Column(db.String(100))
    cost = db.Column(db.Integer)
    done = db.Column(db.Boolean)
    creator = db.Column(db.String(50))
    owner = db.Column(db.String(50))
    creationTime = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)

def __init__(self, id, title, description, cost, done, creator, owner, creationTime, deadline):
    self.id = id
    self.title = title
    self.description = description
    self.cost = cost
    self.done = done
    self.creator = creator
    self.owner = owner
    self.creationTime = creationTime
    self.deadline = deadline

