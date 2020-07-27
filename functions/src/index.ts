import * as functions from 'firebase-functions'
import * as admin from 'firebase-admin'
admin.initializeApp()

// Hello world 
export const helloWorld = functions.https.onRequest((req, res) => {
    res.status(200).send('Welcome to Lovebank!')
})

// Invite, Accept - Pairing
exports.pairing = require('./pairing')
// SMS, Email - AWS
exports.aws = require('./aws');
// SMS - Twilio
exports.twilio = require('./twilio');
// Notification using FCM
exports.fcm = require('./fcm');