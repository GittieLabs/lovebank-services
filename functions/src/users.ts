import * as functions from 'firebase-functions'
import * as admin from 'firebase-admin'
import {v4 as uuid4} from 'uuid'

const db = admin.firestore()

// Generate invite code
export const invite = functions.https.onRequest(async (req, res) => {
    try {
        // Parse and decode ID token from Authorization Header
        const id_token = validateHeader(req)
        const decoded_token = await decodeToken(id_token)
        // Check if ID Token's header matches request body ID
        console.log(`request uid: ${req.body.id}`)
        console.log(`token uid:   ${decoded_token.uid}`)
        if (decoded_token.uid != req.body.id){
            throw({status:401, message:'unauthorized'})
        }
        // Check if request is valid
        if (req.method != 'PUT' || req.body.action != 'invite' || !req.body.id || !req.body.mobile){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }
        // Check if user exists
        const user = await db.doc(`users/${req.body.id}`).get()
        if (!user.exists) {
            throw({status:404, message:'User not found'})
        }
        // Check if user is already linked
        if (user.data()?.partnerId){
            throw({status:400, message:'User already has partner and cannot create invite code'})
        }
        // Generate invite code and make sure there are no invites with the same code
        var inviteCode = (uuid4()).slice(0, 5)
        var check = (await db.collection('invites').where('invite_code', '==', inviteCode).get()).docs[0]
        while (check) {
            inviteCode = (uuid4()).slice(0, 5)
            check = (await db.collection('invites').where('invite_code', '==', inviteCode).get()).docs[0]
        }
        // Create or update invite document with new invite code
        const creationTime = admin.firestore.Timestamp.now()
        const next_week_in_seconds = creationTime.seconds+604800 // 604800 seconds in a week
        const expirationTime = admin.firestore.Timestamp.fromMillis(next_week_in_seconds * 1000)
        await db.collection('invites').doc(req.body.id).set({
            'requester_id': req.body.id,
            'invite_code' : inviteCode,
            'mobile': req.body.mobile,
            'creation_time': creationTime,
            'expiration_time': expirationTime
        })
        const invite_doc = await db.doc(`invites/${req.body.id}`).get()

        res.status(200).send(invite_doc.data())
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

// Accept invite code
export const accept = functions.https.onRequest(async(req, res) => {
    try {
        // Parse and decode ID token from Authorization Header
        const id_token = validateHeader(req)
        const decoded_token = await decodeToken(id_token)
        // Check if ID Token's header matches request body ID
        console.log(`request uid: ${req.body.id}`)
        console.log(`token uid:   ${decoded_token.uid}`)
        if (decoded_token.uid != req.body.id){
            throw({status:401, message:'unauthorized'})
        }
        // Check if request is valid
        if (req.method != 'PUT' || !req.body.id || !req.body.code){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }
        // Check if invite document exists and has not expired
        const inviteRef = db.collection('invites').where('invite_code', '==', req.body.code)
        const invite = (await inviteRef.get()).docs[0]
        const currentTime = Date.now() // Unix time in milliseconds
        if (!invite || (invite.data().expiration_time.seconds * 1000) < currentTime) {
            throw({status:400, message:'Invalid invite code - may be incorrect or expired'})
        }
        // Check if users exist
        const requesterID = invite.data().requester_id
        const receiverID = req.body.id
        const requester = await db.doc(`users/${requesterID}`).get()
        const receiver = await db.doc(`users/${receiverID}`).get()
        if (!requester.exists || !receiver.exists){
            throw({status:404, message:'User not found'})
        }
        // Check if user is trying to link with self
        if (requesterID === receiverID){
            throw({status:400, message:'Cannot link user with self'}) 
        }
        // Check if either user already has partner
        if (requester.data()?.partnerId || receiver.data()?.partnerId){
            throw({status:400, message:'User already has partner'})
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

// Helper function to verify user auth token 
async function decodeToken(idToken) {
    try {
        const decodedToken = await admin.auth().verifyIdToken(idToken)
        console.log('Token decoding: Success')
        return decodedToken
    }
    catch (err) {
        return err
    }
}

// Helper function to validate auth header
function validateHeader(req) {
    if (req.headers.authorization && req.headers.authorization.startsWith('Bearer ')){
        return req.headers.authorization.split('Bearer ')[1]
    }
}
