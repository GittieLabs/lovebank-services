
# LoveBank Database Management
All proposed change in schema should be fully tested on local database. Avoid making migrations to remote database as manual updates on remote DB may break CI pipeline 
by causing conflicts or inconsistency when Travis CI auto updates new data model and deploys new Flask app from master branch later on.


To ensure consistency of data stored, please refrain from directly editing schema within database an utilize migration functionality based on Alembic.
## Schema change workflow:
1. Edit in model


2. Generate migration file


3. Upgade local database


4. Testing to make sure everything works


5. Upon merging to master, make sure your migration file generated is based on the NEWEST migration file on master.


6. If tests passed on master branch, Travis CI will deploy the change - DO NOT upgrade remote DB directly


## Local Database Management

### 1. Create database:
Three databases shall be created for this project - production, testing and development. To create a database in PostgreSQL,
entering the psql shell then :
```
create database lovebank_test;
```
You should see:
```
CREATE DATABASE
``` 
as a response of successful creation. Repeat the same step twice for production (lovebank) and development databases (lovebank_dev).

### 2. DB init (Local) - Not required with migration folder exists:
Within the root folder of this project, you shall see a folder named "migrations". If you do, please jump to step 3 directly. If not, then you would need to init database by:
```
python manage.py db init
```
You should see something like this as the response:
```
 Creating directory ~/Documents/lovebank-services/migrations ...  done
  Creating directory ~/Documents/lovebank-services/migrations/versions ...  done
  Generating ~/Documents/lovebank-services/migrations/script.py.mako ...  done
  Generating ~/Documents/lovebank-services/migrations/env.py ...  done
  Generating ~/Documents/lovebank-services/migrations/README ...  done
  Generating ~/Documents/lovebank-services/migrations/alembic.ini ...  done
  Please edit configuration/connection/logging settings in '~/Documents/lovebank-services/migrations/alembic.ini' before proceeding.

```

### 3. DB schema migration (Local)
Schema migration refers to the action of generate the migration file. A migration file needs to be generated every single time if you want to change the database schema. Migration files generated will be stored in "../migrations/versions". MAKE SURE to view it and edit it as the auto-generated migration file is not bullet-proof and may cause errors when you upgrade. 

### To migrate:
Set up .env file for database and place it within subfolder "lovebank_services". Refer to files shared within Keybase for remote database credentials. Your ENV file should look like this:
```
DATABASE_URL="postgresql://{db_user_name}:{DB password}@localhost/lovebank"
APP_SETTINGS="config.TestingConfig" <--- ONLY applies to your flask app connection
SQLALCHEMY_DATABASE_URI="postgresql://{db_user_name}:{DB password}@localhost/lovebank"
SQLALCHEMY_DATABASE_URI_DEV="postgresql://{db_user_name}:{DB password}/lovebank_dev"
SQLALCHEMY_DATABASE_URI_TEST="postgresql://{db_user_name}:{DB password}/lovebank_test"
SQLALCHEMY_REMOTE_URI="postgresql://{db_user_name}:{DB password}@localhost/lovebank"
SQLALCHEMY_REMOTE_URI_DEV="postgresql://{db_user_name}:{DB password}/lovebank_dev"
SQLALCHEMY_REMOTE_URI_TEST="postgresql://{db_user_name}:{DB password}/lovebank_test"
```
Notice APP_SETTINGS here DOES NOT apply to migrations env and it only applies to running Flask App or running Flask tests. 
Upon running manage.py script (to either make migrations or updates), you would need to specify the database by setting APP_SETTINGS by (either TestingConfig, ProductionConfig or TestingConfig) within your commandline tool or terminal:
```
 export APP_SETTINGS="config.TestingConfig"
```
Then, perform migration - this will generate migration file if a change is detected within models:
```
 python manage.py db migrate
```
Check "../migrations/versions" folder and you shall see a new file generated. Make sure you to edit if you suspect the auto-generated migration file is incorrect in anyway.


### 4. DB schema upgrade (Local)
Upgrade refers to the action of altering database schema using the most recent migration file generated in the previous step. Upgrade will flush the change 
in migration files generated to the database. 

### To upgrade:
Again, you need to specify which database to upgrade by running the following command within terminal or commandline tool (either TestingConfig, ProductionConfig or TestingConfig):
```
 export APP_SETTINGS="config.TestingConfig"
```
Then, perform upgrade:
```
python manage.py db upgrade
```


### 5. DB schema rollback (Local)
Rollback functionality will allow you to downgrade to previous migration file schema in case you identified a mistake:

```
python manage.py db downgrade
```

## Remote Database Management
No upgrades should be made with renmote database. Remote database schema is changed automatically upon updates passing tests on master branch.
But you are more than welcomed to use remote DB for testing purposes. Remember to use the testing database by changing the setting APP_SETTINGS in .env file and run the flask application again to reflect the change:
```
APP_SETTINGS="config.TestingRemoteConfig"
```
Now, you are running backend Flask app on your local device with connection to the remote DB!
