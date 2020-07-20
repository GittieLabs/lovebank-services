import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin'
import {v4 as uuid4} from 'uuid'
admin.initializeApp()

const db = admin.firestore() // Reference to the firestore db

// Hello world 
export const helloWorld = functions.https.onRequest((req, res) => {
    res.status(200).send('Welcome to Lovebank!')
})


// Generate invite code
export const invite = functions.https.onRequest(async (req, res) => {
    if (req.method === 'PUT' && req.body.action === 'invite' && req.body.id){
        const inviteCode = uuid4()
        const userRef = db.doc(`users/${req.body.id}`)
        try {
            await userRef.update({"invite-code" : `${inviteCode}`})
            const updated_user = await db.doc(`users/${req.body.id}`).get()
            // TO DO: send invite code to person
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


// Accept invite code
export const accept = functions.https.onRequest(async(req, res) => {
    const inviteRef = db.collection('invites').where('invite-code', '==', req.body.code)
    try {
        const receiverID = req.body.id
        const requesterID = (await inviteRef.get()).docs[0].data().requester_id
        const receiverRef = db.doc(`users/${receiverID}`)
        const requesterRef = db.doc(`users/${requesterID}`)
        // pair the users
        await receiverRef.update({"partner-id": requesterID})
        await requesterRef.update({"partner-id": receiverID})
        res.send("Success")
    }
    catch(err) {
        res.status(400).send({Error: "Invalid invitation code"})
    }  
})
