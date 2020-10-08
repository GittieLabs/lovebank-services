import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
import {v4 as uuid4} from 'uuid';

const db = admin.firestore()

// Generate task document - body should contain requester's userID, task Description, points for the task 
export const create = functions.https.onRequest(async (req, res) => {
    try {
        // Parse and decode id token from Authorization header
        // const id_token = validateHeader(req)
        // const decoded_token = await decodeToken(id_token)

        // Check if token's uid matches request body id
        // if (decoded_token.uid === undefined || decoded_token.uid != req.body.id){
        //     throw({status:401, message:'unauthorized'})
        // }
        // Check if request is valid
        if (req.method != 'PUT' || !req.body.id || !req.body.description || !req.body.points){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }
        // Check if user exists
        const user = await db.doc(`users/${req.body.id}`).get()
        if (!user.exists) {
            throw({status:404, message:'User not found'})
        }
        //check if user has a partner
        if (user.data().partnerId == ""){
            throw({status:400, message:'User is not connected to a partner'})
        }
        // Generate taskID and make sure there are no tasks with the same ID
        var taskID = (uuid4()).slice(0, 12)
        var check = (await db.collection('tasks').where('task_id', '==', taskID).get()).docs[0]
        while (check) {
            taskID = (uuid4()).slice(0, 12)
            check = (await db.collection('tasks').where('task_id', '==', taskID).get()).docs[0]
        }
        // Create a task document
        const creationTime = admin.firestore.Timestamp.now()
        const nextfour_weeks_in_seconds = creationTime.seconds+ (604800 * 4) // 604800 seconds in a week
        const expirationTime = admin.firestore.Timestamp.fromMillis(nextfour_weeks_in_seconds * 1000)
        await db.collection('tasks').doc(taskID).set({
            'requester_id': req.body.id,
            'partner_id': user.data().partnerId,
            'taskID' : taskID,
            'description' : req.body.description,
            'accepted' : false,
            'points': req.body.points,
            'creation_time': creationTime,
            'expiration_time': expirationTime,
            'deleted':false,
            'completed':false
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

// Modify Task  - Header should contain taskID, updated task description, updated points info
export const update = functions.https.onRequest(async (req, res) =>{
    try{
        // Parse and decode id token from Authorization header
        // const id_token = validateHeader(req)
        // const decoded_token = await decodeToken(id_token)

        // Check if token's uid matches request body id
        // if (decoded_token.uid === undefined || decoded_token.uid != req.body.id){
        //     throw({status:401, message:'unauthorized'})
        // }
        if (req.method != 'PUT' || !req.body.taskID || !req.body.description || !req.body.points){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }
        // update the task document
        await db.collection('tasks').doc(req.body.taskID).update({
            'description' : req.body.description,
            'points': req.body.points,
        })
        const task_doc = await db.doc(`tasks/${req.body.taskID}`).get()
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
// Accept a Task - body should have taskID
export const accept = functions.https.onRequest(async (req, res) =>{
    try{
        // Parse and decode id token from Authorization header
        // const id_token = validateHeader(req)
        // const decoded_token = await decodeToken(id_token)

        // Check if token's uid matches request body id
        // if (decoded_token.uid === undefined || decoded_token.uid != req.body.id){
        //     throw({status:401, message:'unauthorized'})
        // }
        if (req.method != 'PUT' || !req.body.taskID){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }
        // Check if task exists in the database 
        const task = db.collection('tasks').doc(req.body.taskID)
        if (!task) {
            throw({status:400, message:'No such task exists in the database'})
        }

        // accept task
        await db.collection('tasks').doc(req.body.taskID).update({
            'accepted':true
        })
        const task_doc = await db.doc(`tasks/${req.body.taskID}`).get()

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
// Mark a Task as completed - body should have taskID
export const complete = functions.https.onRequest(async (req, res) =>{
    try{
        // Parse and decode id token from Authorization header
        // const id_token = validateHeader(req)
        // const decoded_token = await decodeToken(id_token)

        // Check if token's uid matches request body id
        // if (decoded_token.uid === undefined || decoded_token.uid != req.body.id){
        //     throw({status:401, message:'unauthorized'})
        // }
        if (req.method != 'PUT' || !req.body.taskID){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }
        // Check if task exists in the database 
        const task = db.collection('tasks').doc(req.body.taskID)
        if (!task) {
            throw({status:400, message:'No such task exists in the database'})
        }

        // accept task
        await db.collection('tasks').doc(req.body.taskID).update({
            'completed':true
        })
        const task_doc = await db.doc(`tasks/${req.body.taskID}`).get()

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
// Delete a Task - soft Delete -requires taskID in the body
export const soft_delete = functions.https.onRequest(async (req, res) =>{
    try{
        // Parse and decode id token from Authorization header
        // const id_token = validateHeader(req)
        // const decoded_token = await decodeToken(id_token)

        // Check if token's uid matches request body id
        // if (decoded_token.uid === undefined || decoded_token.uid != req.body.id){
        //     throw({status:401, message:'unauthorized'})
        // }
        if (req.method != 'PUT' || !req.body.taskID){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }
        // Check if task exists in the database 
        const task = db.collection('tasks').doc(req.body.taskID)
        if (!task) {
            throw({status:400, message:'No such task exists in the database'})
        }
        // Delete task document
        await db.collection('tasks').doc(req.body.taskID).update({
            'deleted':true
        })
        const task_doc = await db.doc(`tasks/${req.body.taskID}`).get()

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
// Delete a Task - Hard delete -requires taskID in the body
export const del = functions.https.onRequest(async (req, res) =>{
    try{
        // Parse and decode id token from Authorization header
        // const id_token = validateHeader(req)
        // const decoded_token = await decodeToken(id_token)

        // Check if token's uid matches request body id
        // if (decoded_token.uid === undefined || decoded_token.uid != req.body.id){
        //     throw({status:401, message:'unauthorized'})
        // }
        if (req.method != 'PUT' || !req.body.taskID){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }
        // Check if task exists in the database 
        const task = db.collection('tasks').doc(req.body.taskID)
        if (!task) {
            throw({status:400, message:'No such task exists in the database'})
        }

        // Delete task document
        await task.delete()

        res.status(200).send()
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
// async function decodeToken(idToken) {
//     try {
//         const decodedToken = await admin.auth().verifyIdToken(idToken)
//         return decodedToken
//     }
//     catch (err) {
//         return err
//     }
// }

// Helper function to validate auth header
// function validateHeader(req) {
//     if (req.headers.authorization && req.headers.authorization.startsWith('Bearer ')){
//         return req.headers.authorization.split('Bearer ')[1]
//     }
// }