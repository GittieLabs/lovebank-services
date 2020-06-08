import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from lovebank_services import app, db


"""
this script will help manage database schemas, 

refer to README of sub-folder lovebank_services

Make sure you have ENV variable 'APP_SETTINGS' configured:
    production env -> export APP_SETTINGS="config.ProductionConfig"
    test env -> export APP_SETTINGS="config.TestingConfig"
    development env ->  export APP_SETTINGS="config.DevelopmentConfig"
    
Since this script is running within the terminal - APP_SETTINGS in .env does not apply here!
    
"""

print(app.config['SQLALCHEMY_DATABASE_URI']) # print out to check connection sting
print (os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

# Adding migration commands
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()