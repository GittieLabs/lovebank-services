import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin'
import {v4 as uuid4} from 'uuid'
admin.initializeApp()

// Hello World 
export const helloWorld = functions.https.onRequest((req, res) => {
    res.status(200).send('Welcome to Lovebank!')
})

// Function to update users (generate invite code, create a user, or accept an invite code)
export const users = functions.https.onRequest(async (req, res) => {
    const db = admin.firestore()
    switch(req.method) {
        case 'PUT':
            // Generate code
            if (req.body.action === 'invite' && req.body.id) {
                const inviteCode = uuid4()
                const userRef = db.doc(`users/${req.body.id}`)
                try {
                    await userRef.update({"invite-code" : `${inviteCode}`})
                    const updated_user = (await db.doc(`users/${req.body.id}`).get()).data()
                    res.status(200).send(updated_user)
                }
                catch (err) {
                    res.status(500).send({Error: "There was an error in updating user"})
                }
            }
            // Accept using invite code
            else if (req.body.action === 'accept') {
                res.status(200).send({test: 'accept under construction'})
            }
            // Invalid action field
            else {
                res.status(400).send({error: 'Invalid request'})
            }
            break

        case 'POST': 
            res.status(200).send('POST requested')
            break

        default:
            res.status(405).send({error: "Method not allowed"})
            break
    }
})