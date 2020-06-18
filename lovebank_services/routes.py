from flask import jsonify, abort, request, make_response, url_for
from lovebank_services import app, db
from lovebank_services.models import User, Task
from lovebank_services.fake_data import *
from datetime import datetime
import os

GLOBAL_ID = 0


# TASK ROUTES
@app.route("/", methods=['GET'])
def hello():
    return "You have reached the microservice module of LoveBank!"


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return {'Tasks': list(task.serialize() for task in Task.query.all())}


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        return jsonify(task.serialize())
    abort(404)


@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json:
        abort(400)
    task = Task(creator_id=request.json['creator_id'], receiver_id=request.json['receiver_id'],
                title=request.json['title'],
                description=request.json['description'], cost=request.json['cost'], done=False)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.serialize())


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        if 'description' in request.json:
            task.description = request.json['description']
        if 'receiver_id' in request.json:
            task.receiver_id = request.json['receiver_id']
        if 'creator_id' in request.json:
            task.creator_id = request.json['creator_id']
        if 'title' in request.json:
            task.title = request.json['title']
        if 'cost' in request.json:
            task.cost = request.json['cost']

        db.session.commit()
        return jsonify(Task.query.filter_by(id=task_id).first().serialize())
    abort(404)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'result': True})
    abort(404)


# USER ROUTES
@app.route('/users/<String: uid>', methods=['GET'])
def get_user(uid):
    user = User.query.filter_by(firebase_uid=uid).first()
    if user:
        return jsonify(user.serialize())
    abort(404)


@app.route('/users', methods=['POST'])
def create_user():
    if not request.json:
        abort(400)
    user = User(firebase_uid=request.json['firebase_uid'], email=request.json['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())


@app.route('/linkusers', methods=['POST'])
# Need a JSON file specifying the requester firebase_UID and receiver firebase_UID
def link_user():
    if not request.json:
        abort(400)
    user1 = User.query.filter_by(firebase_uid=request.json['requester_firebase_uid']).first()
    user2 = User.query.filter_by(firebase_uid=request.json['receiver_firebase_uid']).first()
    if user1.partner_firebase_uid or user2.partner_firebase_uid:
        return {'Error': 'Invalid request'}
    else:
        user1.partner_firebase_uid = user2.partner_firebase_uid
        user2.partner_firebase_uid = user1.partner_firebase_uid
        user1.partner_id = user2.id
        user2.partner_id = user1.id
        return {'result': 'true'}


@app.route('/delinkusers', methods=['POST'])
# Need a JSON file specifying the requester firebase_UID and receiver firebase_UID
def delink_user():
    if not request.json:
        abort(400)
    user1 = User.query.filter_by(firebase_uid=request.json['requester_firebase_uid']).first()
    user2 = User.query.filter_by(firebase_uid=request.json['receiver_firebase_uid']).first()
    if (user1.partner_firebase_uid != user1.firebase_uid) or (user2.partner_firebase_uid != user1.partner_firebase_uid):
        return {'Error': 'Invalid request'}
    else:
        user1.partner_firebase_uid = None
        user2.partner_firebase_uid = None
        user1.partner_id = 0
        user2.partner_id = 0
        return {'result': 'true'}


# DEV ROUTES
@app.route('/users', methods=['GET'])
def get_user():
    if User.query.all():
        return {'Users': list(user.serialize() for user in User.query.all())}
    return {'Users': []}


@app.route('/populateUser/<int:rows>', methods=['POST'])
def populate_user(rows):
    populate_user_table(rows, True)
    return {'result': 'True'}


@app.route('/populateTask/<int:rows>', methods=['POST'])
def populate_task(rows):
    if User.query.all():
        populate_task_table(rows)
        return {'result': 'True'}
    return {'Error': 'Fill task table failed. No users have been created yet or users have not been linked'}


@app.route('/clearUser', methods=['DELETE'])
def clear_user():
    clear_table(User)
    return {'result': 'true'}


@app.route('/clearTask', methods=['DELETE'])
def clearTask():
    clear_table(Task)
    return {'result': 'true'}
