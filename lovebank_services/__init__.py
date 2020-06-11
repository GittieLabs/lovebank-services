import os
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from firebase_admin import credentials
import firebase_admin

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
db.create_all()


""" Create Engine - This will be used to execute SQL commands """
db_string = ""
if os.environ['APP_SETTINGS'] == "config.TestingConfig":
    db_string = os.environ['SQLALCHEMY_DATABASE_URI_TEST']

elif os.environ['APP_SETTINGS'] == "config.DevelopmentConfig":
    db_string = os.environ['SQLALCHEMY_DATABASE_URI_DEV']

elif os.environ['APP_SETTINGS'] == "config.ProductionConfig":
    db_string = os.environ['SQLALCHEMY_DATABASE_URI']

elif os.environ['APP_SETTINGS'] == "config.TestingRemoteConfig":
    db_string = os.environ['SQLALCHEMY_REMOTE_URI_TEST']

elif os.environ['APP_SETTINGS'] == "config.DevelopmentRemoteConfig":
    db_string = os.environ['SQLALCHEMY_REMOTE_URI_DEV']

elif os.environ['APP_SETTINGS'] == "config.ProductionRemoteConfig":
    db_string = os.environ['SQLALCHEMY_REMOTE_URI']
engine = create_engine(db_string)


from lovebank_services import routes # to avoid circular import issues, leave this below db initialization & creation of engine


""" Connect Firebase Project """
# cred = credentials.Certificate("firebase-key.json") # path to downloaded firebase service key
# firebase_admin.initialize_app(cred)
