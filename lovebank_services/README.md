
# LoveBank Database Management

To ensure consistency of data stored, please refrain from directly editing schema within database an utilize migration functionality based on Alembic.
## Local migration

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

### 2. DB init (Local) - Required when first set up:
Within the root folder of this project, you shall see a folder named "migrations". if not, then you would need to init database by:
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
Set up .env file for database and place it within subfolder "lovebank_services". Your ENV file should look like this:
```
DATABASE_URL="postgresql://{db_user_name}:{DB password}@localhost/lovebank"
APP_SETTINGS="config.TestingConfig"
SQLALCHEMY_DATABASE_URI="postgresql://{db_user_name}:{DB password}@localhost/lovebank"
SQLALCHEMY_DATABASE_URI_DEV="postgresql://{db_user_name}:{DB password}/lovebank_dev"
SQLALCHEMY_DATABASE_URI_TEST="postgresql://{db_user_name}:{DB password}/lovebank_test"
```
Notice APP_SETTINGS here DOES NOT apply to migrations env and it only applies to running Flask App or running Flask tests. 
Upon running manage.py script, you would need to specify the database by setting APP_SETTINGS by (either TestingConfig, ProductionConfig or TestingConfig):
```
 export APP_SETTINGS="config.TestingConfig"
```


With the help of Alembic, one may run migrations with SQLAlchemy. Make all the edits of the model by directly editing models.py file within lovebank_services. Then to reflect the change
you made within that file in the DB:
```
 python manage.py db migrate
```
Alembic will create migration files if it detects a change within schema. Then make the magic happen by:
```
python manage.py db upgrade
```

### 3. DB schema rollback (Local)

To be written...