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
    try {
        // Check if request is valid
        if (req.method != 'PUT' || !req.body.id || !req.body.code){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }
        // Check if invite document exists
        const inviteRef = db.collection('invites').where('invite_code', '==', req.body.code)
        const invite = (await inviteRef.get()).docs[0]
        if (!invite) {
            throw({status:400, message:'Invalid invite code'})
        }
        // Check if users exist
        const requesterID = invite.data().requester_id
        const receiverID = req.body.id
        const requester = await db.doc(`users/${requesterID}`).get()
        const receiver = await db.doc(`users/${receiverID}`).get()
        if (!requester.exists || !receiver.exists){
            throw({status:404, message:'User not found'})
        }
        // Check if user is trying to pair with self
        if (requesterID === receiverID){
            throw({status:400, message:'Cannot pair user with self'}) 
        }
        // Check if both users are unpaired
        if (requester.data()?.partnerId || receiver.data()?.partnerId){
            throw({status:400, message:'User already paired'})
        }
        // Update both partnerIds
        await db.doc(`users/${receiverID}`).update({'partnerId' : requesterID})
        await db.doc(`users/${requesterID}`).update({'partnerId' : receiverID})
        const updated_user = await db.doc(`users/${receiverID}`).get()
        // Delete invite documents associated with either user
        await db.doc(`invites/${requesterID}`).delete()
        await db.doc(`invites/${receiverID}`).delete()

        res.status(200).send(updated_user.data())
    }
    catch (err) {
        var status = 500
        var message = err
        if (err.status && err.message){
            status = err.status
            message = err.message
        }
        res.status(status).send({"Error": message})
    }
})
