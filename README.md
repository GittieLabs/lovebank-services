# Lovebank Cloud Functions
Cloud functions for Lovebank App

## Getting Started
### 1) Make sure Node.js and npm are installed. If you haven't already installed, you can do so [here](https://nodejs.org/en/)
To check if you have installed Node.js, run:
```
node -v
```
To check if you have installed npm, run:
```
npm -v
```

### 2) Use npm to install the Firebase CLI
```
npm install -g firebase-tools
```

### 3) Login to Firebase using the CLI
``` 
firebase login
```
### 4) Select the project you wish to work on
To view the list of projects (and their IDs) associated with your current account, run
```
firebase projects:list
```
To switch to a project, run the following command - replace {project_id} with the ID of your project:
```
firebase use {project_id}
```
### 5) Install dependencies
Within the "**/functions**" directory, run:
```
npm install
```
## Adding Functions 
Functions are currently declared in the TypeScript file located at "functions/src/index.ts"

## Running Cloud Functions Locally 
Within the "**/functions**" directory, run:
```
npm run serve
```
This will start the functions emulator and deploy them locally. For HTTPS functions, follow the URIs provided to trigger them.

<br/><br/>

## Deploying Cloud Functions
To be written...

<br/><br/>

## Using Cloud Functions
### Create Invite Codes (POST)
Send a **POST** request to the URI for the invite function. The request body should be a JSON object with the following parameters:
##### Parameters
|          Name | Required |   Type  | Description |
| -------------:|:--------:|:-------:| ----------- |
| `id`          | required | string  | id of the user sending the invite |
| `mobile`      | required | string  | mobile number for invitee |
| `action`      | required | string  | should be set to "invite" |

##### Example Request 
```
{
    "id": "AAA4JAwXrwGeoTlZVuz",
    "mobile": "+12345678901",
    "action": "invite"
}
```
If the request is successful, a document will be added or updated in the **invites** collection. The response will be a JSON representation of this invite document.
##### Example Response
```
{
    "creation_time": {
        "_seconds": 1595478889,
        "_nanoseconds": 320000000
    },
    "expiration_time": {
        "_seconds": 1596083689,
        "_nanoseconds": 0
    },
    "requester_id": "AAA4JAwXrwGeoTlZVuz",
    "invite_code": "731b7db1",
    "mobile": "+12345678901"
}
```
Note: The **creation_time** and **expiration_time** fields are created using Firestore timestamps. For more information on Firestore timestamps please refer to [this documentation](https://firebase.google.com/docs/reference/js/firebase.firestore.Timestamp).
<br/><br/>
### Accepting Invites (PUT)
Send a **PUT** request to the URI for the accept function. The request body should be a JSON object with the following parameters:
##### Parameters
|          Name | Required |   Type  | Description |
| -------------:|:--------:|:-------:| ----------- |
| `id`          | required | string  | id of the user accepting the invite |
| `code`        | required | string  | invite code |

##### Example Request 
```
{
    "code": "731b7db1",
    "id": "BBB86GaIFXBxRxyUZc3"
}
```
If the request is successful, the **partnerId** field for both users will be updated accordingly. The response will be a JSON object of the updated user document.
##### Example Response
```
{
    "balance": 0,
    "displayName": "Bob",
    "partnerId": "AAA4JAwXrwGeoTlZVuz",
    "email": "bob@test.com",
    "mobile": "+12345678901"
}
```
