
# LoveBank Services

Services framework for the LoveBank App
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

### 3. Run the run.py file
```
$ python run.py
```
- "Hello, World!" should load on port 5000 (http://localhost:5000/)
- If message loads successfully, then the flask app is running and a database has been initialized locally
- Use CTRL-C to stop running app
##### Note: If you get an error or to reset the database (delete the db file and re-initialize), run the reset_db.py file
```
$ python reset_db.py
```

<br/><br/> 

## Testing the Database
### Using the Unit Test:
To test the SQLite database created locally, run the test_db.py file.
```
$ python test_db.py
```
This test creates 2 user and 2 task objects using the User and Task models defined in ***lovebank_services/models.py***. It adds the objects to the database, then makes queries to check if they were added. Once the test is done, the objects will not exist in the database because this test does not commit them to the database.
<br/>
### Using API Endpoints:
- ### GET
  - [tasks/](#get-tasks)
  - [tasks/{task_id}](#get-taskstask_id)
- ### POST 
  - [tasks/](#post-tasks)
- ### PUT
  - [tasks/{task_id}](#put-taskstask_id)
- ### DELETE
  - [tasks/{task_id}](#delete-taskstask_id)

<br/><br/> 

#### `GET /tasks`
This will return a JSON object of all the tasks in the database. It will be a key value pair, where the key is 'Tasks' and the value is a list of task objects.

<br/><br/> 

#### `GET /tasks/{task_id}`
Replace {task_id} with the id of desired task. It will return a JSON object representing the specified task

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

#### `PUT /tasks/{task_id}`
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

#### `DELETE /tasks/{task_id}`
Replace {task_id} with the ID of the task you want to delete. If the delete was successful, you will see the response below.                                    

###### Example Response
```
{
  "result": true
}
```

## Testing and Integration Pipeline
Upon publishing new commits and merging branches, Travis CI will be triggered to perform tests and then build the new application. If all the tests passed, the updated application will be deployed automatically as well. 

As of now, LoveBank service is deployed at Heroku: https://lovebank.herokuapp.com
