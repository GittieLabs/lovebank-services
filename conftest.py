import pytest

from lovebank_services import create_app, db
from lovebank_services.models import User

''' pytest fixtures to be used by pytest files '''

@pytest.fixture(scope='module')
def new_user():
    user = User(username='Ann', email='ann@test.com')
    return user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
    
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    # This is where testing happens
    yield testing_client  # yield statement provides fixture values and executes teardown code

    ctx.pop()

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
