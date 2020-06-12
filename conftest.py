import pytest

from lovebank_services import app, db
from lovebank_services.models import User

""" config of pytest fixtures to be used by pytest files  """

@pytest.fixture(scope='module')
def test_client():
    """ sets up a testable instance of flask app """
    flask_app = app

    # disable error catching during request handling, so that you get better error reports
    flask_app.config['TESTING'] = True

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
    
    # This is where testing happens
    yield testing_client  # yield statement provides fixture values and executes teardown code

""" 
Fixtures that may be used testing db and user model

@pytest.fixture(scope='module')
def new_user():
    user = User(username='Ann', email='ann@test.com')
    return user

@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(username='Ann', email='ann@test.com')
    user2 = User(username='Bob', email='bob@test.com')
    # Add to DB
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    # This is where testing happens
    yield db  # yield statement provides fixture values and executes teardown code

    db.drop_all() 
    
# Test User Model
def test_User(new_user):
    '''
    GIVEN a User model
    WHEN a new User is created
    THEN check fields are defined correctly
    '''
    assert new_user.email == 'ann@test.com'
    assert new_user.username == 'Ann'
    
    """

