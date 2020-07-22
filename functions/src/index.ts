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
    if (req.method === 'POST' && req.body.action === 'invite' && req.body.id && req.body.mobile){
        const inviteCode = uuid4() // Create invite code
        const user = await db.doc(`users/${req.body.id}`).get()
        if (user.exists) {
            await db.collection('invites').doc(req.body.id).set({
                'requester_id': req.body.id,
                'invite_code' : inviteCode,
                'mobile': req.body.mobile
            })
            const invite_doc = await db.doc(`invites/${req.body.id}`).get()
            res.status(200).send(invite_doc.data())
        }
        else {
            res.status(404).send({Error: 'User not found'})
        }   
    }
    else {
        res.status(400).send({
            Error: 'Bad request. Request may be missing user id, action, or mobile.'
        })
    }
})


// Accept invite code
export const accept = functions.https.onRequest(async(req, res) => {
    if (req.method === 'PUT' && req.body.id && req.body.code) {
        const inviteRef = db.collection('invites').where('invite_code', '==', req.body.code)
        const invite_data = (await inviteRef.get()).docs[0].data()
        if (invite_data) { // Check if invite document exists
            try {
                const requesterRef = db.doc(`users/${invite_data.requester_id}`)
                const receiverRef = db.doc(`users/${req.body.id}`)
                // Update both partnerIds
                await receiverRef.update({'partnerId' : invite_data.requester_id})
                await requesterRef.update({'partnerId' : req.body.id})
                const updated_user = await db.doc(`users/${req.body.id}`).get()
                res.status(200).send(updated_user.data())
            }
            catch(err) {
                res.status(404).send({Error: 'User not found'})
            }
        }
        else {
            res.status(400).send({Error: 'Invalid invite code'})
        }
    }
    else {
        res.status(400).send({
            Error: 'Bad request. Request may be missing user id or invite code.'
        })
    }
})
