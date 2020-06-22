from lovebank_services import db
from lovebank_services.models import User, Task
import os

''' clear data from db and re-initialize '''
class resetDB:
    def reset():
        db.create_all()
        #os.remove("lovebank_services/test.db")
        db.create_all()
        print('db reset successful')

if __name__ == "__main__":
    resetDB.reset()
