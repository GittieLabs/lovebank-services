import unittest
from lovebank_services import db
from lovebank_services.models import User

''' Unit testing for database '''

class TestDB(unittest.TestCase):
    # Test User Model
    def test_User(self):

        print(User.query.all())
        User.query.delete()
        # Create 2 user records
        user_1 = User(username='Ann', email='ann@test.com')
        user_2 = User(username='Bob', email='bob@test.com')
        # Add to DB
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()
        # Query by username
        test_user_1 = User.query.filter_by(username='Ann').first()
        test_user_2 = User.query.filter_by(username='Bob').first()
        # Check if query returns correct user
        self.assertEqual(user_1, test_user_1)
        self.assertEqual(user_2, test_user_2)


if __name__ == '__main__':
    unittest.main()
