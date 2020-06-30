from lovebank_services import firebase_admin as fb_admin

firestore_db = fb_admin.firestore.client()

def compose_update(uid, fid):
    """this function will check with firestore and determine if there's an update to user's task stack
    compose the notification when update detected"""
    title = "none"
    body = " "
    # TO DO
    
    return title, body

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
        response = fb_admin.messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent update notification:', response)
    except: # a lot of errors to handle - for instance new device token and old one no longer valid
        print('Update notification failed to send')
    # [END send_to_token]