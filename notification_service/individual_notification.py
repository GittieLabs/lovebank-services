import firebase_admin
from firebase_admin import messaging, credentials

cred = credentials.Certificate("love-bank-9a624-firebase-adminsdk-r81q1-9c75f8d0dc.json") # shared within keybase
firebase_admin.initialize_app(cred)

def send_to_token(device_token):
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.
    registration_token = 'YOUR_REGISTRATION_TOKEN'

    # See documentation on defining a message payload.
    notification = messaging.Notification(
        title="test notification title",
        body="test notification body"
    )

    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        notification=notification,
        token=device_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_token]

send_to_token("insert token here")