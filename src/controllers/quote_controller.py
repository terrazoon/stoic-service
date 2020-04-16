import json
import uuid
from random import randrange

import boto3
from boto3.dynamodb.conditions import Key

from src.services.email_service import EmailService


dynamodb = boto3.resource('dynamodb', "us-east-1")
table = dynamodb.Table('quotes')

def _get_image(image_data):
    image = f"<div><image src='{image_data}' alt='image'</div>"
    return image


def stoic_quote(event, context):

    response = table.scan(Limit=1)

    items = response['Items']
    quote = items[0]
    print(f"here is quote {quote}")
    table.delete_item(Key={"quote": quote["quote"]})
    table.put_item(TableName='quotes', Item={'quote': quote['quote'], 'author': quote['author'], 'guid': quote['guid']})
    # EmailService.send_email(quote)

    response = {
        "statusCode": 200,
        "body": json.dumps(response)
    }
    return response


def add_quotes(event, context):
    body = event['body']
    body = body.replace("\n", "")
    body = json.loads(body)
    quotes = body["quotes"]

    for quote in quotes:
        response = table.query(
            KeyConditionExpression=Key('quote').eq(quote['quote'])
        )
        print(response)
        if response.get("Count") == 0:
            table.put_item(TableName='quotes', Item={
                'quote': quote['quote'],
                'author': quote['author'],
                'guid': str(uuid.uuid4())
            })

    response = {
        "statusCode": 200,
        "body": json.dumps(quotes)
    }
    return response
