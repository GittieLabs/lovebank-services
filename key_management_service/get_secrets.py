# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import os
import boto3
import base64
import json
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()
region_name = "us-east-2"

# Create a Secrets Manager client
session = boto3.session.Session(aws_access_key_id=os.getenv("AWS_ACCESS_ID"),
                                aws_secret_access_key=os.getenv("AWS_ACCESS_KEY"))
client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)


def get_secret(secret_name):
    """
    given secret name, return secret with each secret string can have multiple secret id/ value pairs

    :param secret_name:
    :return: a dict with desired secret string
    """

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

def list_all_secret_names():
    """
    # all secrets id/value should be stored WITHIN secret name "lovebank-secret"

    :return: a list of all secrets stored on AWS
    """

    response = client.list_secrets()
    response_list = []
    for secret_entry in response["SecretList"]:
        response_list.append(secret_entry["Name"])
    return response_list


def insert_new_secret_pair(secret_name, secret_key, secret_value):
    """
    given a secret, insert a new secret key and value pair into that secret

    :param secret_name: name of secret you intend to insert new secret id/value pair into
    :param secret_key: the name of new secret key to insert, should be all capital letters
    :param secret_value: the value of new secret value to insert
    :return: NONE
    """

    secrets_dict = json.loads(get_secret(secret_name))
    secrets_dict[secret_key] = secret_value
    new_secret_str = json.dumps(secrets_dict)
    response = client.update_secret(SecretId=secret_name,  SecretString=new_secret_str)
    return


if __name__ == "__main__":
    print(get_secret("lovebank-secret"))
    print(list_all_secret_names())
    insert_new_secret_pair("lovebank-secret", "TEST1", "test1")