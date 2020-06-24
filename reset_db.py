from lovebank_services import db
from lovebank_services.models import User, Task
import os

''' clear data from db and re-initialize
 notice this script ONLY clears the table within APP_SETTING specified in env file!'''

def reset():
    Task.query.delete()
    User.query.delete()
    db.session.commit()
    print('db reset successful')

def clear_tables():
    db.drop_all()
    # drop all does not drop table alembic_version, which keeps track of current DB version

if __name__ == "__main__":
    clear_tables()
