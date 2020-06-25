from flask import jsonify, abort, request, make_response, url_for
from lovebank_services import app, db
from lovebank_services.models import User, Task
from lovebank_services.fake_data import *
from datetime import datetime
from uuid import uuid4
import os
import re

uuid_pattern = re.compile('^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')


@app.route("/", methods=['GET'])
def hello():
    return "You have reached the microservice module of LoveBank!"


# TASK ROUTES
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return {'Tasks': list(task.serialize() for task in Task.query.all())}

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

@app.route('/tasks', methods=['DELETE'])
def clearTask():
    clear_table(Task)
    return {'result': 'true'}

@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        return jsonify(task.serialize())
    abort(404)

@app.route('/tasks/<string:task_id>', methods=['PUT'])
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

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'result': True})
    abort(404)


# USER ROUTES
@app.route('/users', methods=['GET'])
def get_users():
    if User.query.all():
        return {'Users': list(user.serialize() for user in User.query.all())}
    return {'Users': []}

@app.route('/users', methods=['POST'])
def create_user():
    if not request.json:
        abort(400)
    if request.json.get('populate', False):
        rows = request.json['populate']
        return populate_user(rows)
    user = User(firebase_uid=request.json['firebase_uid'], email=request.json['email'], username=request.json['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route('/users', methods=['DELETE'])
def clear_user():
    clear_table(User)
    return {'result': 'true'}

@app.route('/users/<string:fid>', methods=['GET'])
def get_user(fid):
    is_uuid = uuid_pattern.match(fid)
    if is_uuid is None:
        user = User.query.filter_by(firebase_uid=fid).first()
    else:
        user = User.query.filter_by(id=fid).first()
    if user:
        return jsonify(user.serialize())
    abort(404)

@app.route('/users/<string:uid>', methods=['PUT'])
def modify_user(uid):
    if not request.json:
        abort(400)
    if request.json.get('action', False):
        print(request.json['action'])
        act = request.json['action']
        if act == 'invite':
            return get_code(request, uid)
        elif act == 'accept':
            return link_user(request, uid)
        elif act == 'unlink':
            return unlink_user(request, uid)
    abort(400)

@app.route('/users/<string:uid>', methods=['DELETE'])
def delete_user(uid):
    #TODO: unlink in firebase as well
    user = User.query.filter_by(id=uid).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'result': True})
    abort(404)


# Generates a unique invite code
def get_code(request, uid):
    if uid and uid != '':
        user = User.query.filter_by(id=uid).first()
        if user:
            if user.partner_id:
                return {'Error': 'User already has a partner'}
            # create list of active invite codes - it will be used to ensure uniqueness of generated code
            active_codes = [item[0] for item in db.session.query(User.invite_code).filter(User.invite_code != None).all()]
            # generate new invite code
            new_code = str(uuid4())[:8] # slice to keep length at 8
            # if code already exist, generate new code until unique code is found
            while new_code in active_codes:
                new_code = str(uuid4())[:8]
            user.invite_code = new_code
            db.session.commit()
            return jsonify(user.serialize())
        return {'Error' : 'User not found'}
    abort(400)

# Need a JSON object specifying the invite code
def link_user(request, uid):
    if not request.json or 'invite_code' not in request.json or uid == '':
        abort(400)
    # find requester with invite code
    user1 = User.query.filter_by(invite_code=request.json['invite_code']).first()
    # if requester is not found, invitation code is invalid
    if not user1:
        return {'Error': 'Invalid invitation code'}
    # find receiver with id passed in JSON object
    user2 = User.query.filter_by(id=uid).first()

    if user1.partner_id or user2.partner_id or user1.id == user2.id:
        return {'Error': 'Invalid request'}
    else:
        user1.partner_id = user2.id,
        user2.partner_id = user1.id,
        # Nullify invite_codes after users are paired
        user1.invite_code = None
        user2.invite_code = None
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        return jsonify(user2.serialize())

# Need a JSON file specifying the receiver firebase_UID
def unlink_user(request, uid):
    if not request.json or uid == '':
        abort(400)
    user1 = User.query.filter_by(id=uid).first()
    user2 = User.query.filter_by(id=user1.partner_id).first()
    if (user1.partner_id != user2.id) or (user2.partner_id != user1.id) or not user2:
        return {'Error': 'Invalid request'}
    #the delink request is only valid when the two users are connected to each other already
    else:
        user1.partner_id = None
        user2.partner_id = None
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        return {'result': 'true'}


# DEV ROUTES

def populate_user(rows):
    populate_user_table(rows)
    return {'result': 'True'}


# @app.route('/populateTask/<int:rows>', methods=['POST'])
# def populate_task(rows):
#     if User.query.all():
#         populate_task_table(rows)
#         return {'result': 'True'}
#     return {'Error': 'Fill task table failed. No users have been created yet or users have not been linked'}
