from lovebank_services import firebase_admin as fb_admin

firestore_db = fb_admin.firestore.client()

def send_to_device(device_token, title, body):
    """this function will send notification only to one device with token specified"""
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.

    # See documentation on defining a message payload.
    notification = fb_admin.messaging.Notification(
        title=title,
        body=body
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
        print('Successfully sent message:', response)
    except: # a lot of errors to handle - for instance new device token and old one no longer valid
        print('Message failed to send')
    # [END send_to_token]

def send_to_user(user_token, title, body):
    """this function will take user UID in firebase and end to each device of this user known"""

    users_ref = firestore_db.collection(u'user_collection').document(user_token).collection(u'device')
    all_devices = users_ref.stream()

    for device in all_devices:
        send_to_device(device.id, title, body)
