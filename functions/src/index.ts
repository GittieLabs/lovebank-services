import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin'
import {v4 as uuid4} from 'uuid'
admin.initializeApp()

// Hello world 
export const helloWorld = functions.https.onRequest((req, res) => {
    res.status(200).send('Welcome to Lovebank!')
})

// Generate invite code
export const users = functions.https.onRequest(async (req, res) => {
    if (req.method === 'PUT' && req.body.action === 'invite' && req.body.id){
        const db = admin.firestore()
        const inviteCode = uuid4()
        const userRef = db.doc(`users/${req.body.id}`)
        try {
            await userRef.update({"invite-code" : `${inviteCode}`})
            const updated_user = await db.doc(`users/${req.body.id}`).get()
            res.status(200).send(updated_user.data())
        }
        catch(err) {
            const errorID = uuid4()           // Create error id
            console.log(`${errorID}: ${err}`) // Log error
            res.status(500).send({Error: `There was an error in updating user. Error ID: ${errorID}`})
        }
    }
    else {
        res.status(400).send({Error: "Bad request"})
    }
})
