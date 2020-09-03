import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
import {v4 as uuid4} from 'uuid';

const db = admin.firestore()

// Generate task document
export const task = functions.https.onRequest(async (req, res) => {
    try {
        // Parse and decode id token from Authorization header
        const id_token = validateHeader(req)
        const decoded_token = await decodeToken(id_token)

        // Check if token's uid matches request body id
        if (decoded_token.uid === undefined || decoded_token.uid != req.body.id){
            throw({status:401, message:'unauthorized'})
        }
        // Check if request is valid
        if (req.method != 'PUT' || !req.body.id || !req.body.mobile){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }
        // Check if user exists
        const user = await db.doc(`users/${req.body.id}`).get()
        if (!user.exists) {
            throw({status:404, message:'User not found'})
        }
        // Check if user is already linked
        if (user.data()?.partnerId){
            // throw({status:400, message:'User already has partner and cannot create invite code'})
        }
        else{
            throw({status:400, message:'User has no partner to create a task'})
        }
        // Generate invite code and make sure there are no invites with the same code
        var taskID = (uuid4()).slice(0, 12)
        var check = (await db.collection('tasks').where('task_id', '==', inviteCode).get()).docs[0]
        while (check) {
            taskID = (uuid4()).slice(0, 12)
            check = (await db.collection('invites').where('invite_code', '==', inviteCode).get()).docs[0]
        }
        // Create or update invite document with new invite code
        const creationTime = admin.firestore.Timestamp.now()
        const nextfour_weeks_in_seconds = creationTime.seconds+604800 * 4 // 604800 seconds in a week
        const expirationTime = admin.firestore.Timestamp.fromMillis(nextfour_weeks_in_seconds * 1000)
        await db.collection('invites').doc(taskID).set({
            'requester_id': req.body.id,
            'partner_id': req.body.partnerid,
            'taskID' : taskID,
            'description' : req.body.description,
            'accepted' : false,
            'points': req.body.points,
            'creation_time': creationTime,
            'expiration_time': expirationTime
        })
        const task_doc = await db.doc(`tasks/${taskID}`).get()

        res.status(200).send(task_doc.data())
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