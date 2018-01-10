from flask import jsonify, request
from flask_api import status, exceptions

from flask import request
from flask_api import FlaskAPI, status
from app.models import Task


from app.config import app, db
from app.models import Task
from app.errors import InvalidParameter, TaskNotFound
from sqlalchemy.exc import IntegrityError

import logging


@app.route('/tasks/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        tasks = Task.query.all()
        results = [t.to_json() for t in tasks]
        return results, status.HTTP_201_CREATED

    elif request.method == 'POST':
        if 'task_name' in request.data:
            task_name = request.data['task_name']
            try:
                if task_name:
                    new_task = Task(task_name=task_name)
                    db.session.add(new_task)
                    db.session.commit()
                    response = new_task.to_json()
                    return response, status.HTTP_201_CREATED
            except IntegrityError:
                return {'error': 'This task already exists'}
        raise InvalidParameter


@app.route('/tasks/<int:id>/', methods=['GET', 'DELETE'])
def manage_tasks(id):
    task = Task.query.filter_by(id=id).first()
    if not task:
        raise TaskNotFound
    if request.method == 'GET':
        response = task.to_json()
        return response
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return {
            'message': 'task deleted'
        }


if __name__ == '__main__':
    db.create_all()
    logging.basicConfig(
        filename='error.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app.run(debug=True)
    app.run(debug=True)
