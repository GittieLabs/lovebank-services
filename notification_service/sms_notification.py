import os
import boto3
import base64
import json
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()
region_name = "us-east-1" # not all AWS region supports SMS

# Create a SNS client
session = boto3.session.Session(aws_access_key_id=os.getenv("AWS_ACCESS_ID"),
                                aws_secret_access_key=os.getenv("AWS_ACCESS_KEY"))
client = session.client(
    service_name='sns',
    region_name=region_name
)

# Phone number format - "+" then 10 digits in a single str

def send_sms_customized(target_number, message):
    response = client.publish(PhoneNumber=target_number, Message=message)
    return response

def send_sms_invite_code(target_number, code):
    message_str = f'Welcome to LoveBank. Here is your invite code to connect with your partner: {code}'
    response = client.publish(PhoneNumber=target_number, Message=message_str)
    return response