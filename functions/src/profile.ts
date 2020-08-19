import * as functions from 'firebase-functions'
import * as admin from 'firebase-admin'

const db = admin.firestore()

// Revoke invitation
export const profilePic = functions.https.onRequest(async(req, res) => {
    try {
        // Parse and decode id token from Authorization header
        const id_token = validateHeader(req)
        const decoded_token = await decodeToken(id_token)

        // Check if request is valid
        if (req.method != 'PUT' || !req.body.id || !req.body.fileURL){
            throw({status:400, message:'Request field may be missing or incorrect method used'})
        }

        // Check if token's uid matches request body id
        if (decoded_token.uid != req.body.id){
        throw({status:401, message:'unauthorized'})
        }

        // Check if user exists in the database 
        const userRef = db.doc(`users/${req.body.id}`)
        const user = await userRef.get()
        if (!user.exists) {
            throw({status:404, message:'User not found'})
        }

        // Get the current profile URL
        const currentURL = user.data().profilePic   

        // Update user's profile url 
        await userRef.update({
            'profilePic': req.body.fileURL,
        })

        res.status(200).send(currentURL)
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
