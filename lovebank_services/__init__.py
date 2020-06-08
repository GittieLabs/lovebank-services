import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from flask_migrate import Migrate
from firebase_admin import credentials
import firebase_admin

load_dotenv() # Specify which env by setting .env file

# Initialize Flask app
app = Flask(__name__)

# Set location of database
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # avoid SQLAlchemy warning messages

# Create a database instance - Note: test.db will by ignored by .gitignore. Update file if necessary
db = SQLAlchemy(app)
db.create_all()
from lovebank_services import routes # to avoid circular import issues, leave this import below initializatoin of db
print(app.config['SQLALCHEMY_DATABASE_URI'])
''' To connect to Firebase project - uncomment below and point to service key path '''
# cred = credentials.Certificate("firebase-key.json") # path to downloaded firebase service key
# firebase_admin.initialize_app(cred)
