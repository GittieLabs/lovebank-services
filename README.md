
# LoveBank Services
[![Build Status](https://travis-ci.com/GittieLabs/lovebank-services.svg?branch=master)](https://travis-ci.com/GittieLabs/lovebank-services)

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

## Testing the Database
To test the SQLite database created locally, run the test_db.py file.
```
$ python test_db.py
```
This test creates two user objects using the User model defined in ***lovebank_services/models.py***. It adds the user objects to the database, then makes queries to check if they were added. Once the test is done, the objects will not exist in the database because this test does not commit them to the database.
