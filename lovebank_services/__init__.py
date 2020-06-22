import os
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from firebase_admin import credentials
import firebase_admin
from key_management_service.get_secrets import *



load_dotenv() # Specify which env by setting .env file

""" Initialize Flask App """
app = Flask(__name__)


""" Set Location of Database """
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # avoid SQLAlchemy warning messages
print(os.environ['APP_SETTINGS'])


""" Create a Database Instance """
db = SQLAlchemy(app)
from lovebank_services.models import Task, User
# db.create_all() # Please create tables using migrations by running manage.py


""" Create Engine - This will be used to execute SQL commands """
db_string = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(db_string)


db.create_all() # Please create tables using migrations by running manage.py
from lovebank_services import routes # to avoid circular import issues, leave this import below initializatoin of db

from lovebank_services import routes # to avoid circular import issues, leave this below db initialization & creation of engine


""" Connect to Firebase Project Using KMS - Uncomment below """
secret_name = "lovebank-secret"
response = get_secret(secret_name)
secret_dict = json.loads(response)
try:
    cred = credentials.Certificate(json.loads(secret_dict['FIREBASE_SERVICE_KEY'])) # path to downloaded firebase service key
    firebase_admin.initialize_app(cred)
    print("Firebase Connection Successful")
except:
    print("Error: Firebase Connection Unsuccessful")
