import firebase_admin
from firebase_admin import messaging, credentials, firestore

cred = credentials.Certificate("love-bank-9a624-firebase-adminsdk-r81q1-9c75f8d0dc.json") # shared within keybase
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

def send_to_device(device_token, title, body):
    """this function will send notification only to one device with token specified"""
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.

    # See documentation on defining a message payload.
    notification = messaging.Notification(
        title=title,
        body=body
    )

    message = messaging.Message(
        notification=notification,
        token=device_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_token]

def send_to_user(user_token, title, body):
    """this function will take user UID in firebase and end to each device of this user known"""

    users_ref = firestore_db.collection(u'user_collection').document(user_token).collection(u'device')
    all_devices = users_ref.stream()

    for device in all_devices:
        send_to_device(device.id, title, body)

