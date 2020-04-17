import json
import os
import random

import boto3

from src.services.email_service import EmailService

dynamodb = boto3.resource('dynamodb', "us-east-1")
email_table = dynamodb.Table('emailAddresses')

s3 = boto3.resource('s3')


def get_quotes(object_name):
    obj = s3.Object("vvhvhvh-stoic-service-dev", object_name)
    body = obj.get()['Body'].read()
    body = json.loads(body)
    quotes = body['Quotes']
    return quotes


seneca_quotes = get_quotes("quotes/seneca.json")
epictetus_quotes = get_quotes("quotes/epictetus.json")
marcus_quotes = get_quotes("quotes/marcus_aurelius.json")

# Get the service resource
sqs = boto3.client('sqs')
# Get the queue. This returns an SQS.Queue instance
queue_url = os.environ["POSTING_QUEUE_URL"]


def _get_image(image_data):
    image = f"<div><image src='{image_data}' alt='image'</div>"
    return image


def stoic_quote(event, context):
    """
    Get the list of emails in the database and add them
    to the PostingQueue for daily processing
    :param event:
    :param context:
    :return:
    """
    response = email_table.scan()
    data = response['Items']
    for item in data:
        email_address = item['email']
        my_response = sqs.send_message(QueueUrl=queue_url, MessageBody=email_address)
        print(f"posted to sqs queuee {item}")

    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }
    return response


def process_email(event, context):
    """
    Take an individual email address and send the quote to it

    :param event:
    :param context:
    :return:
    """
    records = event['Records']
    record = records[0]
    my_email_address = record['body']

    quotes = _pick_author()
    num = len(quotes)
    my_rand = random.randint(0, num - 1)
    quote = quotes[my_rand]
    EmailService.send_email(quote, my_email_address)
    response = {
        "statusCode": 200,
        "body": json.dumps(event)
    }
    return response


def _pick_author():
    my_rand = random.choice(['seneca', 'epictetus', "marcus_aurelius"])
    print(f"MY AUTHOR = {my_rand}")
    if my_rand == 'seneca':
        return seneca_quotes
    elif my_rand == 'marcus_aurelius':
        return marcus_quotes
    else:
        return epictetus_quotes

