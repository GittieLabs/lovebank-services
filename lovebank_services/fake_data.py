import os
import random
from faker import Faker
from dotenv import load_dotenv
from lovebank_services import db, engine, User, Task

def populate_user_table(rows, linked):
    """
    This method populates the User table with the number of rows
    specified by the parameter. If linked = true, the users will be linked to each other.
    Based on the logic of this method, if rows = 10, user 1 will be lined to user 10,
    user 2 will be linked to user 9...
    If linked = false, the users won't be linked to each other (partner_id = NULL)
    :param linked: if true, tables will be filled with linked users; if false, the partner_id column will be None.
    :param rows: number of rows to be populated
    :return: None
    """
    f = Faker()

    if not linked or rows == 1:
        # set all partner_id = None if linked is false.
        partner_id_value = None
    else:
        # Retrieve the largest user_id in db
        partner_id_value = db.session.query(func.max(User.id)).scalar()
        print(str(partner_id_value))
        if not partner_id_value:
            partner_id_value = rows
        else:
            partner_id_value += rows

    for i in range(rows):
        db.session.add(User(partner_id=partner_id_value, username=f.name(), email=f.email()))
        if partner_id_value:
            partner_id_value -= 1

    db.session.commit()


def populate_task_table(rows):
    """
    This method populates the task table with the number of rows
    specified by the parameter. Each task will get a random creator, a paired receiver, title, description, and cost.
    Accepted, deadline and done are set to default values.
    :param rows: number of rows to be populated
    :return: None
    """

    max_creator_id = db.session.query(func.max(User.id)).scalar()
    max_partner_id = db.session.query(func.max(User.partner_id)).scalar()

    # If no users exist yet, an error message will be returned
    if not max_creator_id or not max_partner_id:
        print('Error: Fill task table failed. \nNo users have been created yet or users have not been linked.')

    f = Faker()
    sample_tasks = ['buy groceries', 'do something', 'Wash dishes', 'feed the baby', 'walk the dog',
                    'watch netflix with me']

    for i in range(rows):
        rand_creator_id = f.pyint(min_value=1, max_value=max_creator_id)
        rand_receiver_id = User.query.get(rand_creator_id).partner_id
        rand_title = random.choice(sample_tasks)
        # Random cost differs by 50 (50 <= cost <= 500)
        rand_cost = f.pyint(min_value=50, max_value=500, step=50)
        db.session.add(Task(creator_id=rand_creator_id, receiver_id=rand_receiver_id,
                            title=rand_title, description='Just do it', cost=rand_cost))
    db.session.commit()


def clear_table(model):
    """
    This method takes a given table and clears all rows of data from it,
    while preserving the data schema.
    :param model: the model to be cleared
    :return: None
    """
    # if model not in (User, Task):
    #     print('Error: please enter either User or Task for clear_table().')
    #     quit()
    # db.session.query(model).delete()
    # db.session.commit()

    if model == Task:
        engine.execute("DROP TABLE task;")
    if model == User:
        engine.execute('DROP TABLE "user" CASCADE;')
    db.create_all()
