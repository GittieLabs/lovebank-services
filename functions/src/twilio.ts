import * as functions from "firebase-functions";
import * as admin from 'firebase-admin';
require('dotenv').config(); // ENV file should be placed within functions folder

export function publish_sms_twilio(message, phone_number){ //phone number must be 10 digits and start with +
    const accountSid = process.env.TW_SID;
    const authToken = process.env.TW_AUTH_TOKEN;
    const client = require('twilio')(accountSid, authToken);
    
    client.messages
      .create({
         body: message,
         from: '+19375435043', //DONT CHANGE - purchased num from Twilio for lovebank project
         to: phone_number
       })
      .then(message => console.log(message.sid));
}

export const invite_text = functions.firestore.document('invites/{invite_id}').onCreate(async (change, context) => {
  //required fields in invite collection: mobile, requester_id
  //required document: doc with doc_id as requester_id in users collection
  //required field in users collection: displayName 

  console.log("Detetected new invitation!");
  const invite_str = `${change.data().invite_code}`;
  const phone_number_str = change.data().mobile;
  const inviter_doc = admin.firestore().collection('users').doc(change.data().requester_id);
  const inviter_name = await inviter_doc.get().then(document => {
    return document.data().displayName;
  })


  try{
    const text = `${inviter_name} wants to connect with you on LoveBank! Here is the invitation code: ${invite_str}`;
    publish_sms_twilio(text, phone_number_str);
  }catch(e){
    console.log(e)
  }

  return true;
 });
