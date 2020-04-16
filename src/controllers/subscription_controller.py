import json

import boto3

dynamodb = boto3.resource('dynamodb', "us-east-1")
table = dynamodb.Table('emailAddresses')


def subscribe(event, context):
    email = event['pathParameters']['email']

    response = table.get_item(
        Key={
            'email': email
        }
    )

    if response.get("Item") is None:
        table.put_item(TableName='emailAddresses', Item={'email': email})

    response = {
        "statusCode": 200,
        "body": json.dumps(email)
    }
    return response


def unsubscribe(event, context):

    email = event['pathParameters']['email']

    response = table.delete_item(
        Key={
            'email': email
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(email)
    }
    return response
