import unittest
from uuid import UUID

from lovebank_services import db
from lovebank_services.models import User, Task
from datetime import datetime

''' Unit testing for database '''

class Test_Task(unittest.TestCase):
    # Clear user and task tables within database
    Task.query.delete()
    User.query.delete()
    # setUp runs before every test
    def setUp(self):
        # Create 2 user records and add them to db
        self.user_1 = User(username='Ann', id="1cf96ab3-f693-4909-9d32-067438bc9636",
                           partner_id="49dcc18d-0e6b-43a7-82c3-c8396fc77ee5",
                           email='ann@test.com')
        self.user_2 = User(username='Bob', id="49dcc18d-0e6b-43a7-82c3-c8396fc77ee5",
                           partner_id="1cf96ab3-f693-4909-9d32-067438bc9636",
                           email='bob@test.com')
        db.session.add(self.user_1)
        db.session.add(self.user_2)
        db.session.commit()
        # Create 2 task records and add them to db
        self.task_1 = Task(creator_id="1cf96ab3-f693-4909-9d32-067438bc9636",
                           receiver_id="49dcc18d-0e6b-43a7-82c3-c8396fc77ee5",
                           title='title_1',
                           description='description_1',
                           cost=10,
                           deadline=datetime.fromtimestamp(1596477600))
        self.task_2 = Task(creator_id="49dcc18d-0e6b-43a7-82c3-c8396fc77ee5",
                           receiver_id="1cf96ab3-f693-4909-9d32-067438bc9636",
                           title='title_2',
                           description='description_2',
                           cost=25,
                           deadline=datetime.fromtimestamp(1608442620))
        db.session.add(self.task_1)
        db.session.add(self.task_2)
        db.session.commit()

    # tearDown runs after every test
    def tearDown(self):
        # Delete users and tasks
        Task.query.filter_by(creator_id="1cf96ab3-f693-4909-9d32-067438bc9636").delete()
        Task.query.filter_by(creator_id="49dcc18d-0e6b-43a7-82c3-c8396fc77ee5").delete()
        User.query.filter_by(username = 'Ann').delete()
        User.query.filter_by(username = 'Bob').delete()

    def test_Task(self):
        # Query by titles
        test_task_1 = Task.query.filter_by(title='title_1').first()
        test_task_2 = Task.query.filter_by(title='title_2').first()
        # Check if query returns correct task
        print("task testing")
        self.assertEqual(self.task_1, test_task_1)
        self.assertEqual(self.task_2, test_task_2)


class Test_User(unittest.TestCase):
    # Clear user and task tables within database
    User.query.delete()
    # setUp runs before every test
    def setUp(self):
        # Create 2 user records and add them to db
        self.user_1 = User(username='Ann', id="1cf96ab3-f693-4909-9d32-067438bc9636",
                           partner_id="49dcc18d-0e6b-43a7-82c3-c8396fc77ee5",
                           email='ann@test.com', balance=10)
        self.user_2 = User(username='Bob', id="49dcc18d-0e6b-43a7-82c3-c8396fc77ee5",
                           partner_id="1cf96ab3-f693-4909-9d32-067438bc9636",
                           email='bob@test.com', balance=20)
        db.session.add(self.user_1)
        db.session.add(self.user_2)
        db.session.commit()


    # tearDown runs after every test
    def tearDown(self):
        # Delete users and tasks
        User.query.filter_by(id="1cf96ab3-f693-4909-9d32-067438bc9636").delete()
        User.query.filter_by(id="49dcc18d-0e6b-43a7-82c3-c8396fc77ee5").delete()

    # 1) Test User Model
    def test_User(self):
        # Query by usernames
        test_user_1 = User.query.filter_by(id="1cf96ab3-f693-4909-9d32-067438bc9636").first().__dict__
        test_user_2 = User.query.filter_by(id="49dcc18d-0e6b-43a7-82c3-c8396fc77ee5").first().__dict__
        # Check if query returns correct user
        # Cannot directly compare user instance - assertEqual will fail as they have two object num
        self.assertEqual(10, test_user_1['balance'])
        self.assertEqual('ann@test.com', test_user_1['email'])
        self.assertEqual('Ann', test_user_1['username'])
        self.assertEqual(20, test_user_2['balance'])
        self.assertEqual('bob@test.com', test_user_2['email'])
        self.assertEqual('Bob', test_user_2['username'])

if __name__ == '__main__':
    unittest.main()
