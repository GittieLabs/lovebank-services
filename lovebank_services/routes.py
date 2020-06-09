from flask import jsonify, abort, request, make_response, url_for
from lovebank_services import app, db
from lovebank_services.models import User, Task
from datetime import datetime
import os

# TASK ROUTES
@app.route("/", methods=['GET'])
def hello():
    return "You have reached the microservice module of LoveBank!"


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return {'Tasks' : list(task.serialize() for task in Task.query.all())}


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
    task = Task(creator_id=request.json['creator_id'], receiver_id=request.json['receiver_id'], title=request.json['title'],
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
