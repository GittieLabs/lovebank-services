from lovebank_services import db     # imports db variable from __init__.py
from datetime import datetime

# User Model
class User(db.Model):
    ''' Define User model '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# Task Model
class Task(db.Model):
    ''' Define Task model '''
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

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer)
    done = db.Column(db.Boolean)
    creator = db.Column(db.String(80))
    owner = db.Column(db.String(80))
    creationTime = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)

    def __repr__(self):
        return 'Task(id: %d, title: %s, description: %s, cost: %d)' % (self.id, self.title, self.description, self.cost)

