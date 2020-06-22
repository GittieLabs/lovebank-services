import unittest
from lovebank_services import db
from lovebank_services.models import User, Task
from datetime import datetime

''' Unit testing for database '''

class TestDB(unittest.TestCase):
    # Clear user and task tables within database
    User.query.delete()
    Task.query.delete()
    # setUp runs before every test
    def setUp(self):
        # Create 2 user records and add them to db
        self.user_1 = User(username='Ann', id=1, partner_id=2, email='ann@test.com')
        self.user_2 = User(username='Bob', id=2, partner_id=1, email='bob@test.com')
        db.session.add(self.user_1)
        db.session.add(self.user_2)
        db.session.commit()
        # Create 2 task records and add them to db
        self.task_1 = Task(creator_id=1, receiver_id=2, title='title_1', description='description_1', cost=10, deadline=datetime.fromtimestamp(1596477600))
        self.task_2 = Task(creator_id=2, receiver_id=1, title='title_2', description='description_2', cost=25, deadline=datetime.fromtimestamp(1608442620))
        db.session.add(self.task_1)
        db.session.add(self.task_2)
        db.session.commit()

    # tearDown runs after every test
    def tearDown(self):
        # Delete users and tasks
        Task.query.filter_by(creator_id=1).delete()
        Task.query.filter_by(creator_id=2).delete()
        User.query.filter_by(username = 'Ann').delete()
        User.query.filter_by(username = 'Bob').delete()

    # 1) Test User Model
    def test_User(self):
        # Query by usernames
        test_user_1 = User.query.filter_by(username='Ann').first()
        test_user_2 = User.query.filter_by(username='Bob').first()
        # Check if query returns correct user
        self.assertEqual(self.user_1, test_user_1)
        self.assertEqual(self.user_2, test_user_2)

    # 2) Test Task Model
    def test_Task(self):
        # Query by titles
        test_task_1 = Task.query.filter_by(title='title_1').first()
        test_task_2 = Task.query.filter_by(title='title_2').first()
        # Check if query returns correct task
        self.assertEqual(self.task_1, test_task_1)
        self.assertEqual(self.task_2, test_task_2)


if __name__ == '__main__':
    unittest.main()