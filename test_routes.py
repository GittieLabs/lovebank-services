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


@pytest.mark.skip(reason="Utility function")
def create_test_user(test_client, email):
    """
        utility function to create a test user
    """

    # delete test user in firebase if already exists
    try:
        user = auth.get_user_by_email(email)
        auth.delete_user(user.uid)
    except:
        pass

    user = auth.create_user(email=email, password="12345678")
    fid = user.uid

    response = test_client.post('/users', data=json.dumps({'firebase_uid': fid,
                                                           'username': email + ' username',
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
    #Set a flag for test functions that depend on creation/deletion working
    test_client.create_delete_success = False

    email = "test@pytest.pytest"

    response = create_test_user(test_client, email)
    response_data = json.loads(response.get_data(as_text=True))
    assert(response.status_code == 200)

    uid = response_data['id']

    response = delete_test_user(test_client, uid)
    response_data = json.loads(response.get_data(as_text=True))

    assert(response.status_code == 200)
    assert(response_data["result"] == True)

    #Set a flag for test functions that depend on creation/deletion working
    test_client.create_delete_success = True

def test_get_users(test_client):
    """
    GIVEN a flask application
    WHEN the /users/id endpoint is called with GET using UUID or firebase id
    THEN check the user returns successfully
    """

    #Set a flag for test functions that depend on creation/deletion/getting working
    test_client.get_create_delete_success = False

    #Test depends on creation/deletion
    assert(test_client.create_delete_success)

    #get users should be an empty list or a list with users
    response = test_client.get('/users')
    response_data = json.loads(response.get_data(as_text=True))
    assert(response.status_code == 200)
    assert(response_data.get("Users", False) and type(response_data["Users"]) is list)

    old_users = response_data["Users"]

    #create a user
    response = create_test_user(test_client, "test2@pytest.pytest")
    response_data = json.loads(response.get_data(as_text=True))
    uid = response_data['id']
    fid = response_data['firebase_uid']

    #get the user individually both by uid and firebase_uid
    response = test_client.get('/users/'+uid)
    uid_user = json.loads(response.get_data(as_text=True))
    response = test_client.get('/users/'+fid)
    fid_user = json.loads(response.get_data(as_text=True))
    assert("id" in uid_user.keys())
    assert("firebase_uid" in uid_user.keys())
    assert("partner_id" in uid_user.keys())
    assert("username" in uid_user.keys())
    assert("email" in uid_user.keys())
    assert("balance" in uid_user.keys())
    assert("invite_code" in uid_user.keys())
    assert(uid_user == fid_user)

    #get all users and compare to original list
    response = test_client.get('/users')
    response_data = json.loads(response.get_data(as_text=True))

    new_users = response_data["Users"]

    assert(len(old_users) == len(new_users) - 1)

    delete_test_user(test_client, uid)

    #Set a flag for test functions that depend on creation/deletion/getting working
    test_client.get_create_delete_success = True

def test_populate_users(test_client):
    #Test depends on getting/creation/deletion
    assert(test_client.get_create_delete_success)

    #get users
    response = test_client.get('/users')
    response_data = json.loads(response.get_data(as_text=True))
    users = response_data["Users"]

    #populate 3 users
    response = test_client.post('/users', data=json.dumps({"populate":3}), content_type='application/json')
    #get_users again
    response = test_client.get('/users')
    response_data = json.loads(response.get_data(as_text=True))
    new_users = response_data["Users"]

    #make sure there are 3 more users
    populated = [] #list(set(new_users) - set(users))
    for x in new_users:
        match = False
        for y in users:
            if x["id"] == y["id"]:
                match = True
        if match == False:
            populated.append(x)

    assert(len(populated) == 3)

    #for each of the three users, find in firebase
    for x in populated:
        try:
            auth.get_user(x["firebase_uid"])
        except:
            #if the user can't be found in firebase, fail
            assert(False)
        delete_test_user(test_client, x["id"])

def test_invite_accept_unlink_users(test_client):

    #Test depends on getting/creation/deletion
    assert(test_client.get_create_delete_success)

    #create a user
    response = create_test_user(test_client, "test3@pytest.pytest")
    user1 = json.loads(response.get_data(as_text=True))

    response = create_test_user(test_client, "test4@pytest.pytest")
    user2 = json.loads(response.get_data(as_text=True))

    #make sure invite code and partner id is null
    assert(user1["invite_code"] == None)
    assert(user1["partner_id"] == None)

    assert(user2["invite_code"] == None)
    assert(user2["partner_id"] == None)

    #invite user
    response = test_client.put('/users/' + user1["id"], data=json.dumps({"action":"invite"}), content_type="application/json")
    response_data = json.loads(response.get_data(as_text=True))

    assert(user1["id"] == response_data["id"])

    #make sure that invite code exists
    code = response_data["invite_code"]
    assert(code != None)

    #invite again
    response = test_client.put('/users/' + user1["id"], data=json.dumps({"action":"invite"}), content_type="application/json")
    response_data = json.loads(response.get_data(as_text=True))

    #make sure that code is different and not null
    new_code = response_data["invite_code"]
    assert(new_code != None)
    assert(new_code != code)

    #link user to self
    response = test_client.put('/users/' + user1["id"], data=json.dumps({"action":"accept", "invite_code": new_code}), content_type="application/json")

    #ensure that this fails
    response = test_client.get('/users/' + user1["id"])
    temp_user = json.loads(response.get_data(as_text=True))

    assert(temp_user["partner_id"] == None)

    #link two users
    response = test_client.put('/users/' + user2["id"], data=json.dumps({"action":"accept", "invite_code": new_code}), content_type="application/json")
    user2 = json.loads(response.get_data(as_text=True))

    response = test_client.get('/users/' + user1["id"])
    user1 = json.loads(response.get_data(as_text=True))

    assert(user2["partner_id"] == user1["id"])
    assert(user2["invite_code"] == None and user1["invite_code"] == None)

    #invite one of the users
    response = test_client.put('/users/' + user1["id"], data=json.dumps({"action":"invite"}), content_type="application/json")

    #make sure that invite code is still null
    response = test_client.get('/users/' + user1["id"])
    user1 = json.loads(response.get_data(as_text=True))
    assert(user1["invite_code"] == None)

    #check that partner_id on both is linked
    assert(user1["partner_id"] == user2["id"])
    assert(user2["partner_id"] == user1["id"])



    #unlink
    response = test_client.put('/users/' + user1["id"], data=json.dumps({"action":"unlink"}), content_type="application/json")

    response = test_client.get('/users/' + user1["id"])
    user1 = json.loads(response.get_data(as_text=True))

    response = test_client.get('/users/' + user2["id"])
    user2 = json.loads(response.get_data(as_text=True))

    #make sure that invite code is null
    assert(user1["invite_code"] == None and user2["invite_code"] == None)
    #make sure that partner_id is null
    assert(user1["partner_id"] == None and user2["partner_id"] == None)

    delete_test_user(test_client, user1["id"])
    delete_test_user(test_client, user2["id"])
