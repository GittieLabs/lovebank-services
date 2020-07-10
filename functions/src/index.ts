import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin'
// import {v4 as uuid4} from 'uuid'
admin.initializeApp()

// Hello World 
export const helloWorld = functions.https.onRequest((req, res) => {
    res.status(200).send('Welcome to Lovebank!')
})
