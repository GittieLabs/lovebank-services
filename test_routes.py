""" pytest for flask API  
    see conftest.py file for fixture config
"""

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
    response = test_client.get('/tasks/123')
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
    response = test_client.post('/tasks/123')
    assert response.status_code == 405
    assert response.content_type == 'text/html; charset=utf-8'