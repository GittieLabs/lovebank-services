import pytest
from lovebank_services import db
from lovebank_services.models import User

''' pytest for database '''

class TestDB:
    # Test User Model
    def test_User(self):
        db.create_all()
        # Create 2 user records
        user_1 = User(username='Ann', email='ann@test.com')
        user_2 = User(username='Bob', email='bob@test.com')
        # Add to DB
        db.session.add(user_1)
        db.session.add(user_2)
        # Query by username
        test_user_1 = User.query.filter_by(username='Ann').first()
        test_user_2 = User.query.filter_by(username='Bob').first()
        # Check if query returns correct user
        assert user_1 == test_user_1
        assert user_2 == test_user_2