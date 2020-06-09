from lovebank_services import db     # imports db variable from __init__.py
from datetime import datetime, timedelta

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    balance = db.Column(db.Integer)
    tasks_created = db.relationship('Task', backref='creator', lazy=True, foreign_keys='Task.creator_id')
    tasks_received = db.relationship('Task', backref='receiver', lazy=True, foreign_keys='Task.receiver_id')

    def serialize(self):
        ''' return data as dictionary '''
        return {
            "id"        :   self.id,
            "partner_id":   self.partner_id,
            "username"  :   self.username,
            "email"     :   self.email,
            "balance"   :   self.balance,
            "tasks_received": list(task.serialize() for task in self.tasks_received),
            "tasks_created" : list(task.serialize() for task in self.tasks_created)
        }

    def __repr__(self):
        return f"User('username: {self.username}', email: '{self.email}')"


# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creationTime = db.Column(db.DateTime, default=datetime.utcnow())
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.partner_id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    accepted = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(days=1))
    compTime = db.Column(db.DateTime, default=None)
    done = db.Column(db.Boolean, default=False)

    def serialize(self):
        ''' return data as dictionary '''
        return {
            "id"          :   self.id,
            "creationTime":   self.creationTime,
            "creator_id"  :   self.creator_id,
            "receiver_id" :   self.receiver_id,
            "title"       :   self.title,
            "description" :   self.description,
            "cost"        :   self.cost,
            "accepted"    :   self.accepted,
            "deadline"    :   self.deadline,
            "compTime"    :   self.compTime,
            "done"        :   self.done
        }

    def __repr__(self):
        return 'Task(id: %d, title: %s, description: %s, cost: %d)' % (self.id, self.title, self.description, self.cost)
