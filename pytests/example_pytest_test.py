import pytest
from flask import json
from example_flask_app import app

''' simple pytest for a flask API example '''

def test_hello():
    ''' tests GET request '''
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'Hello, World!'

def test_add():
    ''' tests POST request with json response '''
    response = app.test_client().post('/add',
    data=json.dumps({'a': 1, 'b': 2}),
    content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['sum'] == 3

