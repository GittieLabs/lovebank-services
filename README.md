
# LoveBank Services

[![Build Status](https://travis-ci.com/GittieLabs/lovebank-services.svg?branch=master)](https://travis-ci.com/GittieLabs/lovebank-services)

Services framework for the LoveBank App

## Getting Started
Before running the app, there are a few steps that need to be taken. For more thorough guide on database setup, refer to read me in lovebank-services subfolder. <br/>
#### **1.** Create 3 local PostgreSQL databases. You can name them ***lovebank_test***, ***lovebank_dev***, and ***lovebank*** <br/><br/>
#### **2.** Within the ***lovebank_services*** folder, add a **.env** file and include the following (some information is omitted):<br/>
````
APP_SETTINGS="config.TestingRemoteConfig"

SQLALCHEMY_DATABASE_URI_TEST="postgresql://localhost/lovebank_test"
SQLALCHEMY_DATABASE_URI_DEV="postgresql://localhost/lovebank_dev"
SQLALCHEMY_DATABASE_URI="postgresql://localhost/lovebank"

SQLALCHEMY_REMOTE_URI_TEST="postgresql://{username}:{password}@000.000.00.000/lovebank_test"
SQLALCHEMY_REMOTE_URI_DEV="postgresql{username}:{password}@000.000.00.000/lovebank_dev"
SQLALCHEMY_REMOTE_URI="postgresql://{username}:{password}@000.000.00.000/lovebank"
````
- Point the top 3 URIs to the 3 local PostgreSQL databases you created  <br/>
- Point the bottom 3 URIs to the remote PostgreSQL databases (please see Keybase for complete URIs) <br/> 
- **APP_SETTINGS** will determine which database the flask app connects to when run. Refer to the following guide when deciding its value:
    - APP_SETTINGS="config.TestingConfig" will connect to the database referenced by SQLALCHEMY_DATABASE_URI_TEST <br/>
    - APP_SETTINGS="config.DevelopmentConfig" will connect to database referenced by SQLALCHEMY_DATABASE_URI_DEV  <br/>
    - APP_SETTINGS="config.ProductionConfig" will connect to the database referenced by SQLALCHEMY_DATABASE_URI   <br/>
    - APP_SETTINGS="config.TestingRemoteConfig" will connect to the database referenced by SQLALCHEMY_REMOTE_URI_TEST <br/>
    - APP_SETTINGS="config.DevelopmentRemoteConfig" will connect to database referenced by SQLALCHEMY_REMOTE_URI_DEV  <br/>
    - APP_SETTINGS="config.ProductionRemoteConfig" will connect to the database referenced by SQLALCHEMY_REMOTE_URI   <br/>

#### **3.** Within the ***key_management_service*** folder, add another **.env** file and include the following (some information is omitted):<br/>
```
AWS_ACCESS_ID={ACCESS_KEY_HIDDEN}
AWS_ACCESS_KEY={ACCESS_KEY_HIDDEN}
```
Please refer to keybase for access keys

 <br/><br/>

## Running the Flask app
To avoid dependency conflicts, it is best to use a virtual environment to run the app.
### 1. Create and run virtual environment:
#### Mac and Linux:
```
$ python3 -m venv venv
$ source venv/bin/activate
```
Detailed instructions: https://www.youtube.com/watch?v=Kg1Yvry_Ydk

#### Windows:
```
$ py -3 -m venv venv
$ venv\Scripts\activate.bat
```
Detailed instructions: https://www.youtube.com/watch?v=APOPm01BVrk

### 2. Install the requirements:
```
$ pip install -r requirements.txt
```

### 3. Run the app.py file
```
$ python app.py
```
- "You have reached the microservice module of LoveBank!" should load on port 5000 (http://localhost:5000/)
- If message loads successfully, then the flask app is running and a database has been initialized locally
- Use CTRL-C to stop running app


<br/><br/>

## Testing the Database
### Using the Unit Test:
To test postgres database locally, run the test_db.py file. This will only test the DB specified in your APP_SETTINGS in .env file.
```
$ python test_db.py
```

This test creates 2 user and 2 task objects using the User and Task models defined in ***lovebank_services/models.py***. It adds the objects to the database, then makes queries to check if they were added. Once the test is done, the objects will not exist in the database because this test does not commit them to the database.

### Using pytest:
To test the Flask API routes, run the test_routes.py file.
```
$ python3 -m pytest -k test_routes.py
```
***test_routes.py*** tests the API routes and requests defined in ***lovebank_services/__init__.py***. Note that the the test_client which calls a test version of the Flask app gets set in ***conftest.py*** (pytest's preferred default name for the config file). 

pytest can also run all tests it automatically detects with this command.
```
$ python3 -m pytest
```

<br/>

### Using API Endpoints:
- ### GET
  - [/tasks](#get-tasks)
  - [/tasks/{task_id}](#get-taskstask_id)
  - [/users](#get-users)
  - [/users/{firebase_id}](#get-usersfirebase_id)
- ### POST
  - [/tasks](#post-tasks)
  - [/users](#post-users)
- ### PUT
  - [/tasks/{task_id}](#put-taskstask_id)
  - [/users/{user_id}](#put-usersuser_id)
- ### DELETE
  - [/tasks](#delete-tasks)
  - [/tasks/{task_id}](#delete-taskstask_id)
  - [/users](#delete-users)
  - [/users/{user_id}](#delete-usersuser_id)

<br/><br/>

#### `GET /tasks`
This will return a JSON object of all the tasks in the database. It will be a key value pair, where the key is 'Tasks' and the value is a list of task objects.

<br/><br/>

#### `GET /tasks/{task_id}`
Replace {task_id} with the id of desired task. It will return a JSON object representing the specified task

<br/><br/>

#### `GET /users`
This will return a JSON object of all the users in the database. It will be a key value pair, where the key is 'Users' and the value is a list of user objects.

<br/><br/>

#### `GET /users/{firebase_id}`
Replace {firebase_id} with the firebase id (or the UUID) of desired user. Whether firebase id or UUID is used is automatically detected. It will return a JSON object representing the specified user

<br/><br/>

#### `POST /tasks`
Add a task using the parameters sent in the request body (JSON).
##### Parameters
|          Name | Required |   Type  | Description |
| -------------:|:--------:|:-------:| ----------- |
| `creator_id` | required | integer | ID number of account that created the task |
| `receiver_id`| required | integer | ID number of account receiving the task |
| `cost`       | required | integer | Integer representing the value of the task |
| `title`      | required | string  | String of max length 50 representing the title of task |
| `description`| required | string  | String of max length 120 describing the task |

##### Example Response
###### The response will be a representation of the task created
```
{
  "cost": 50,
  "creationTime": "Fri, 05 Jun 2020 02:53:59 GMT",
  "creator_id": 1,
  "description": "cook a romantic dinner, guess my favorite dish",
  "done": false,
  "id": 3,
  "receiver_id": 2,
  "title": "cook dinner"
}
```
<br/><br/>

#### `POST /users`
If parameter `"populate": {number}` and `"linked": {linked}"` is in the request body (JSON):\
Populate the users table with `{number}` more people.\
Populate the users table with linked users if `{linked}` is true, and unlinked users if `{linked}` is false.\

The following provided JSON will populate 2 linked users in the database.
```
{
    "populate": 2,
    "linked": true
}
```

Otherwise:
Add a user using the parameters sent in the request body (JSON).
##### Parameters
|          Name | Required |   Type  | Description |
| -------------:|:--------:|:-------:| ----------- |
| `firebase_uid`| required | string  | Firebase ID of user to be created |
| `email`       | required | string  | Email of user to be created |
| `username`    | required | string  | Username of user to be created |

##### Example Response
###### The response will be a representation of the task created
```
{
    "balance": 500,
    "email": "xyz@gmail.com",
    "firebase_uid": "8ZriE8QTQ6Mmm6PbZH6nSwiEjjkL",
    "id": "8e7c264d-0730-4fd3-bf77-4029a95e5eb8",
    "invite_code": null,
    "partner_firebase_uid": null,
    "partner_id": null,
    "tasks_created": [],
    "tasks_received": [],
    "username": "georges"
}
```
<br/><br/>

#### `PUT /tasks/{task_id}`
Modify a task based on the parameters in the request body (JSON).
##### Parameters
|          Name | Required |   Type  | Description |
| -------------:|:--------:|:-------:| ----------- |
| `creator_id` | optional | integer | ID number of account that created the task |
| `receiver_id`| optional | integer | ID number of account receiving the task |
| `cost`       | optional | integer | Integer representing the value of the task |
| `title`      | optional | string  | String of max length 50 representing the title of task |
| `description`| optional | string  | String of max length 120 describing the task |

##### Example Response
###### The response will be a representation of the task updated
```
{
  "cost": 75,
  "creationTime": "Fri, 05 Jun 2020 03:08:45 GMT",
  "creator_id": 2,
  "description": "walk with me and Mr.Fluffers more often",
  "done": false,
  "id": 4,
  "receiver_id": 1,
  "title": "take walks with me and our dog"
}
```
<br/><br/>

#### `PUT /users/{user_id}`
Modify a user in different ways based on the `"action": {act}` parameter in the request body (JSON).

If `"action": "invite"`:
Sets the invite code on the user with the specified user id.
##### Parameters
|          Name | Required |   Type  | Description |
| -------------:|:--------:|:-------:| ----------- |
| `action`      | required | string  | Must be "invite" for this action |

##### Example Response
###### The response will be a representation of the user updated
```
{
    "balance": 500,
    "email": "brandonmorrow@yahoo.com",
    "firebase_uid": "Vw5FWxAXGwaSDEne2S58a2Nz12k2",
    "id": "c525d250-b7e3-492c-a943-99b428c95af0",
    "invite_code": "9085d9b4",
    "partner_firebase_uid": null,
    "partner_id": null,
    "tasks_created": [],
    "tasks_received": [],
    "username": "James Smith"
}
```

If `"action": "accept"`:
Links the user with the specified user id to the user with the invite code in the request body (JSON).
##### Parameters
|          Name | Required |   Type  | Description |
| -------------:|:--------:|:-------:| ----------- |
| `action`      | required | string  | Must be "accept" for this action |
| `invite_code` | required | string  | The invite code of the user to link to |

##### Example Response
###### The response will be a representation of the user updated
```
{
    "balance": 500,
    "email": "elizabethvance@mcdonald.com",
    "firebase_uid": "3zJvUANil5IKUDcJmOOb34C0o552",
    "id": "fa38add0-b691-4710-9d7d-7474945b9c56",
    "invite_code": null,
    "partner_firebase_uid": "Vw5FWxAXGwaDuhSECS58a2Nz12k2",
    "partner_id": "c525d250-b7e3-492c-a943-99b428c95af0",
    "tasks_created": [],
    "tasks_received": [],
    "username": "Cody James"
}
```

If `"action": "unlink"`:
Unlinks the user with the specified user id from their partner and also unlinks their partner.
##### Parameters
|          Name | Required |   Type  | Description |
| -------------:|:--------:|:-------:| ----------- |
| `action`      | required | string  | Must be "unlink" for this action |

##### Example Response
###### The response will be the following if unlinking was successful.
```
{
    "result": "true"
}
```

<br/><br/>

#### `DELETE /tasks`
To clear the Task table, run a DELETE request to the endpoint above. If the delete was successful, you will see the response below.

###### Example Response
```
{
  "result": true
}
```

<br/><br/>

#### `DELETE /tasks/{task_id}`
Replace {task_id} with the ID of the task you want to delete. If the delete was successful, you will see the response below.

###### Example Response
```
{
  "result": true
}
```

<br/><br/>

#### `DELETE /users`
To clear the User table, run a DELETE request to the endpoint above. If the delete was successful, you will see the response below.

###### Example Response
```
{
  "result": true
}
```

<br/><br/>

#### `DELETE /users/{user_id}`
Replace {user_id} with the ID of the user you want to delete. If the delete was successful, you will see the response below.

###### Example Response
```
{
  "result": true
}
```

<br/><br/>

## Testing and Integration Pipeline
Upon publishing new commits and merging branches, Travis CI will be triggered to perform tests and then build the new application. If all the tests passed, the updated application will be deployed automatically as well. 

As of now, LoveBank service is deployed at Heroku: https://lovebank.herokuapp.com
