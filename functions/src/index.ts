import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin'
admin.initializeApp()

// Hello World 
export const helloWorld = functions.https.onRequest((req, res) => {
    res.status(200).send('Welcome to Lovebank!')
})