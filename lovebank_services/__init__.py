from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from firebase_admin import credentials
import firebase_admin

# Initialize Flask app
app = Flask(__name__)
from lovebank_services import routes # to avoid circular imports, leave this import below initializatoin of app

# Set location of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # test.db will be created in this file directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # avoid SQLAlchemy warning messages

# Create a database instance - Note: test.db will by ignored by .gitignore. Update file if necessary
db = SQLAlchemy(app)
db.create_all()

''' To connect to Firebase project - uncomment below and point to service key path '''
# cred = credentials.Certificate("firebase-key.json") # path to downloaded firebase service key
# firebase_admin.initialize_app(cred)
