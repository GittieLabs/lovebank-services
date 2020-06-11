import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from firebase_admin import credentials
import firebase_admin


load_dotenv() # Specify which env by setting .env file


''' Initialize Flask App '''
app = Flask(__name__)


''' Set Location of Database '''
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # avoid SQLAlchemy warning messages
print(os.environ['APP_SETTINGS'])


''' Create a Database Instance ''''
db = SQLAlchemy(app)
from lovebank_services.models import Task, User
db.create_all()
from lovebank_services import routes # to avoid circular import issues, leave this import below initializatoin of db


''' Connoect Firebase Project '''
# cred = credentials.Certificate("firebase-key.json") # path to downloaded firebase service key
# firebase_admin.initialize_app(cred)
