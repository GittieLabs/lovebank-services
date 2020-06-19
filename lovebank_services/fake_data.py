import os
import random
from faker import Faker
from dotenv import load_dotenv
from lovebank_services import db, engine, User, Task
from sqlalchemy import func
from firebase_admin import auth


def populate_user_table(rows):
    """
    This method populates the User table with the number of rows specified.
    It will create the number of users in firebase as well.
    All created users will not be linked.
    :param rows: number of rows to be populated
    :return: None
    """
    f = Faker()

    for i in range(rows):
        userEmail = f.email()
        user = auth.create_user(email=userEmail, password="12345678")
        uid = user.uid
        db.session.add(User(firebase_uid=uid, username=f.name(), email=userEmail))

    db.session.commit()


# def populate_task_table(rows):
#     """
#     This method populates the task table with the number of rows
#     specified by the parameter. Each task will get a random creator, a paired receiver, title, description, and cost.
#     Accepted, deadline and done are set to default values.
#     :param rows: number of rows to be populated
#     :return: None
#     """
#
#     max_creator_id = db.session.query(func.max(User.id)).scalar()
#     max_partner_id = db.session.query(func.max(User.partner_id)).scalar()
#
#     # If no users exist yet, an error message will be returned
#     if not max_creator_id or not max_partner_id:
#         print('Error: Fill task table failed. \nNo users have been created yet or users have not been linked.')
#
#     f = Faker()
#     sample_tasks = ['buy groceries', 'do something', 'Wash dishes', 'feed the baby', 'walk the dog',
#                     'watch netflix with me']
#
#     for i in range(rows):
#         rand_creator_id = f.pyint(min_value=1, max_value=max_creator_id)
#         rand_receiver_id = User.query.get(rand_creator_id).partner_id
#         rand_title = random.choice(sample_tasks)
#         # Random cost differs by 50 (50 <= cost <= 500)
#         rand_cost = f.pyint(min_value=50, max_value=500, step=50)
#         db.session.add(Task(creator_id=rand_creator_id, receiver_id=rand_receiver_id,
#                             title=rand_title, description='Just do it', cost=rand_cost))
#     db.session.commit()


def clear_table(model):
    """
    This method takes a given table and clears all rows of data from it,
    while preserving the data schema.
    The users in firebase will be deleted as well.
    :param model: the model to be cleared
    :return: None
    """

    if model == Task:
        db.session.query(Task).delete()
    if model == User:
        db.session.query(Task).delete()

        # Delete users in the firebase
        for value in db.session.query(User.firebase_uid).all():
            val = ''.join(value)
            auth.delete_user(val)

        db.session.query(User).delete()
    db.session.commit()