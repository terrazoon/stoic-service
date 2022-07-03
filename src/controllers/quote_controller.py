import json
import os

import boto3

from src.services.email_service import EmailService
from src.services.quotes_service import QuotesService

dynamodb = boto3.resource('dynamodb', "us-east-1")
email_table = dynamodb.Table('emailAddresses')

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
    #print("stoic quote called")
    response = email_table.scan()
    data = response['Items']
    #print(f"data is {data}")
    _put_email_addresses_in_queue(data)
    while 'LastEvaluatedKey' in response:
        response = email_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data = response['Items']
        _put_email_addresses_in_queue(data)

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

    quote = QuotesService.get_quote()
    #print(f"processing email {my_email_address} {quote}")
    EmailService.send_email(quote, my_email_address)
    response = {
        "statusCode": 200,
        "body": json.dumps(event)
    }
    return response


def _put_email_addresses_in_queue(data):
    #print(f"enter _put_email_addresses_queue with {data}")
    for item in data:
        #print(f"item is {item}")
        email_address = item['email']
        #print(f"putting {email_address} in posting queue")
        my_response = sqs.send_message(QueueUrl=queue_url, MessageBody=email_address)
