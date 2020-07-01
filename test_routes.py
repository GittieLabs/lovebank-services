"""
    pytest for flask API  
    see conftest.py file for fixture config
"""
import pytest
import json
from firebase_admin import auth

def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"You have reached the microservice module of LoveBank!" in response.data

def test_tasks_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/tasks' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/tasks')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

def test_tasks_get_by_id(test_client):
    """
    GIVEN a Flask application
    WHEN the '/tasks/<int:task_id>' page is requested (GET)
    THEN check the response is valid
    """
    # currently will only show that 404 error is generated
    # TO DO: make test with a valid task id to query for
    response = test_client.get('/tasks/1cf96ab3-f693-4909-9d32-067438bc9636')
    assert response.status_code == 404
    assert response.content_type == 'text/html; charset=utf-8'

def test_tasks_post(test_client):
    """
    GIVEN a Flask application
    WHEN the '/tasks' page is posted to (POST)
    THEN check the response is valid
    """
    # currently will only show that 400 error is generated
    # TO DO: configure db fixture in conftest.py & make a POST request with mock data
    response = test_client.post('/tasks')
    assert response.status_code == 400
    assert response.content_type == 'text/html; charset=utf-8'

def test_tasks_post_by_id(test_client):
    """
    GIVEN a Flask application
    WHEN the '/tasks/<int:task_id>' page is posted to (POST)
    THEN check the response is valid
    """
    # currently will only show that 405 error is generated
    # TO DO: configure db fixture in conftest.py & make a POST request with mock data
    response = test_client.post('/tasks/1cf96ab3-f693-4909-9d32-067438bc9636')
    assert response.status_code == 405
    assert response.content_type == 'text/html; charset=utf-8'



### Below is the user endpoints tests.
# DELETE /users (to clear all users) isn't
# tested here due to the risk of accidentally
# clearing all data in the wrong database.

create_delete_success = False

@pytest.mark.skip(reason="Utility function")
def create_test_user(test_client, email):
    """
        utility function to create a test user
    """

    user = auth.create_user(email=email, password="12345678")
    fid = user.uid

    response = test_client.post('/users', data=json.dumps({'firebase_uid': fid, 
                                                           'username': 'create delete pytest',
                                                           'email': email}), content_type='application/json')
    return response


@pytest.mark.skip(reason="Utility function")
def delete_test_user(test_client, uid):
    """
        utility function to delete a test user
    """
    response = test_client.delete('/users/'+uid)
    return response



def test_create_delete_users(test_client):
    """
    GIVEN a flask application
    WHEN the /users endpoint is called with POST or DELETE (individual delete)
    THEN check the user creates and deletes successfully
    """
    email = "test@pytest.pytest"

    response = create_test_user(test_client, email)
    response_data = json.loads(response.get_data(as_text=True))
    assert(response.status_code == 200)

    uid = response_data['id']

    response = delete_test_user(test_client, uid)
    response_data = json.loads(response.get_data(as_text=True))

    assert(response.status_code == 200)
    assert(response_data["result"] == True)

    create_delete_success = True

def test_populate_users():
    pass

def test_get_users():
    pass

def test_invite_users():
    pass

def test_link_users():
    pass

def test_unlink_users():
    pass


