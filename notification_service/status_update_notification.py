from lovebank_services import firebase_admin as fb_admin
from lovebank_services.models import User, Task
from datetime import datetime

firestore_db = fb_admin.firestore.client()

def compose_update(uid, fid):
    """this function will check with firestore and determine if there's an update to user's task stack
    compose the notification when update detected

    if there is no changes detected, a notification will still be composed if update notification was not sent for at least at hour"""
    title = "none"
    body = " "

    doc_ref = firestore_db.collection('update_status').document(fid)
    doc_ref.set({
        u'last_updated': datetime.now(),
        u'message_sent': u'unknown',
    })

    if not doc_ref.get().exists:
        return title, body

    update_doc_ref = firestore_db.collection('update_queue').document(fid)
    update_text = update_doc_ref.get().get('message')
    if update_text == ' ':
        pass
    else:
        title = "LoveBank Task Changed:"
        body = update_text
        update_doc_ref.update({
            u'message': ' '
        })
        doc_ref.update({
            u'message_body': update_text
        })

    return title, body

def add_update(uid, fid, update_text):
    """this function will add a document or update a document on update_queue collection
    update_queue will be used and empties upon generating update notification using compose_update method"""
    doc_ref = firestore_db.collection('update_queue').document(fid)

    if doc_ref.get().exists:
        new_update_text = ' '+ doc_ref.get().get('message') + '\n ' + update_text
        doc_ref.update({
            u'last_updated': datetime.now(),
            u'message': new_update_text
        })
    else:
        doc_ref.set({
            u'created': datetime.now(),
            u'last_updated': datetime.now(),
            u'message': update_text,
        })
    return True

def notify_receiver(uid_task, request):
    """ given task UID,
    find fid for task receiver and call function add_update to add message body for next update notification"""
    task_receiver_id = Task.query.filter_by(id=uid_task).first().receiver_id
    task_receiver = User.query.filter_by(id=task_receiver_id).first()
    update_str = " "

    print(request.json)
    for k, v in request.json.items():
        update_str = update_str + k + " updated: " + v + "\n "

    add_update(task_receiver.id, task_receiver.firebase_uid, update_str)
    return True


def update_notification(uid, fid, device_token):
    """this function will send notification only to one device with token specified
    it should be called automatically when the app is launched - a notification is displayed on flutter is change detected"""
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.

    composed_title, composed_body = compose_update(uid, fid)

    # See documentation on defining a message payload.
    notification = fb_admin.messaging.Notification(
        title=composed_title,
        body=composed_body
    )

    message = fb_admin.messaging.Message(
        notification=notification,
        token=device_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    try:
        if composed_title == "none":
            print("No update notification sent - no change detected")
        else:
            response = fb_admin.messaging.send(message)
            # Response is a message ID string.
            print('Successfully sent update notification:', response)
            doc_ref = firestore_db.collection('update_status').document(fid)
            doc_ref.update({
                u'last_delivery_attempt': datetime.now(),
                u'message_sent': u'success',
            })
    except: # a lot of errors to handle - for instance new device token and old one no longer valid
        print('Update notification failed to send')
        doc_ref = firestore_db.collection('update_status').document(fid)
        doc_ref.update({
            u'last_delivery_attempt': datetime.now(),
            u'message_sent': u'error',
        })
    # [END send_to_token]