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
```
npm install
```
## Adding Functions 
Functions will be added to the TypeScript file located at "functions/src/index.ts"

## Running Cloud Functions Locally 
To be written..

## Deploying Cloud Functions
To be written..
