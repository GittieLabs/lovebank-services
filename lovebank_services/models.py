from lovebank_services import db  # imports db variable from __init__.py
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


# User Model
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(UUID(as_uuid=True), default=uuid4, unique=True, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=True)  # set nullable=True to prevent errors when populating table
    partner_id = db.Column(UUID(as_uuid=True), unique=True)
    partner_firebase_uid = db.Column(db.String(128), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    balance = db.Column(db.Integer, default=0)
    tasks_created = db.relationship('Task', backref='creator', lazy=True, foreign_keys='Task.creator_id')
    tasks_received = db.relationship('Task', backref='receiver', lazy=True, foreign_keys='Task.receiver_id')

    def serialize(self):
        ''' return data as dictionary '''
        return {
            "id": self.id,
            "firebase_uid": self.firebase_uid,
            "partner_id": self.partner_id,
            "partner_firebase_uid": self.partner_firebase_uid,
            "username": self.username,
            "email": self.email,
            "balance": self.balance,
            "tasks_received": list(task.serialize() for task in self.tasks_received),
            "tasks_created": list(task.serialize() for task in self.tasks_created)
        }

    def __repr__(self):
        return f"User('username: {self.username}', email: '{self.email}')"


# Task Model
class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    creationTime = db.Column(db.DateTime, default=datetime.utcnow())
    creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
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
            "id": self.id,
            "creationTime": self.creationTime,
            "creator_id": self.creator_id,
            "receiver_id": self.receiver_id,
            "title": self.title,
            "description": self.description,
            "cost": self.cost,
            "accepted": self.accepted,
            "deadline": self.deadline,
            "compTime": self.compTime,
            "done": self.done
        }

    def __repr__(self):
        return 'Task(id: %d, title: %s, description: %s, cost: %d)' % (self.id, self.title, self.description, self.cost)