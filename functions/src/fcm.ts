import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin'

async function notify_user(uid, notification_title, notification_body){
  // look for user device token in user_collection and send notification to each of the device
  const payload = {notification: {
    title: notification_title,
    body: notification_body
    }};

  const device_collection = await admin.firestore().collection('user_collection').doc(uid).collection('device').get();
  device_collection.forEach(document => {    
    console.log("Send to device with token: ", document.data().token);
    if (process.env['GCLOUD_PROJECT'] == 'love-bank-testing'){
      console.log("Testing ENV - No real FCM sent out");
      return;
    }
    try{
      admin.messaging().sendToDevice(document.data().token, payload);
    }catch(e){
      console.log(e);
    }
  })
  
}

export const task_create_notify = functions.firestore.document('tasks/{task_id}').onCreate(async (change, context) => { 
  console.log("Detected Task Creation!")

  const creator_uid = change.data().creator_id;
  const receiver_uid = change.data().receiver_id;
  const creator_title = `You created a new task - ${change.data().title}`;
  const receiver_title = `You have a new task - ${change.data().title}`
  const notification_body = `Task Description: ${change.data().description}`;

  notify_user(creator_uid, creator_title, notification_body);
  notify_user(receiver_uid, receiver_title, notification_body);
  return true;
 });

export const task_delete_notify = functions.firestore.document('tasks/{task_id}').onDelete((change, context) => {
  console.log("Detected Task Deletion!");

  const creator_uid = change.data().creator_id;
  const receiver_uid = change.data().receiver_id;
  const title = `Task Deleted - ${change.data().title}`;
  const notification_body = `Task Description: ${change.data().description}`;

  notify_user(creator_uid, title, notification_body);
  notify_user(receiver_uid, title, notification_body);
  return true;
});

export const task_update_notify = functions.firestore.document('tasks/{task_id}').onUpdate((change, context) => {
  console.log("Detected Task Update!");
  const creator_uid = change.after.data().creator_id;
  const receiver_uid = change.after.data().receiver_id;
  const changed_task = change.after.data();
  const original_task = change.before.data();

  try{
    if (changed_task.done == true && original_task.done == false){
      const oldBalance = admin.firestore.doc(`users/${changed_task.receiver_id}`).get('balance');
      const newBalance = oldBalance + changed_task.reward;
      admin.firestore.doc(`users/${changed_task.receiver_id}`).update({'balance': newBalance});
    }
    
    
    // implementation not optimal - task description
    if (changed_task.description != original_task.description){
      console.log("Task Description Updated")
      const title = `Task Description Updated - ${changed_task.title}`;
      const notification_body = `New Description: ${changed_task.description}`;

      notify_user(creator_uid, title, notification_body);
      notify_user(receiver_uid, title, notification_body);
    }

  }catch(e){
    console.log(e);
  }

  try{
    // implementation not optimal - task reward 
    if (changed_task.reward != original_task.reward){
      console.log("Task Reward Updated")
      const title = `Task Reward Updated - ${changed_task.title}`;
      const notification_body = `Task Reward has changed ${original_task.reward} from to ${changed_task.reward}`;

      notify_user(creator_uid, title, notification_body);
      notify_user(receiver_uid, title, notification_body);
    }

  }catch(e){
    console.log(e);
  }
  return true;

});

export const user_update_notify = functions.firestore.document('users/{uid}').onUpdate((change, context) => {
  console.log("Detected User Update!");

  const changed_user = change.after.data();
  const original_user = change.before.data();
  const user_id = change.after.id //doc id is user's UID

  try{
    // implementation not optimal - user balance
    if (changed_user.balance != original_user.balance){
      const title = `LoveBank Balance Update`;
      const notification_body = `Your balance has changed ${original_user.balance} from to ${changed_user.balance}`;
      notify_user(user_id, title, notification_body);
    }
  }catch(e){
    console.log(e);
  }
  return true;

});