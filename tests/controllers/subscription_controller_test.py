import unittest

import boto3
import mock
import pytest
from moto import mock_dynamodb, mock_dynamodb2

from src.controllers.subscription_controller import unsubscribe, subscribe


class SubscriptionControllerTest(unittest.TestCase):
    @mock_dynamodb2
    def test_unsubscribe(self):
        table_name = 'emailAddresses'
        dynamodb = boto3.resource('dynamodb', 'us-east-1')
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        event = {"pathParameters": {"email": "abc@x.y"}}

        response = unsubscribe(event, None)
        assert response['statusCode'] == 200
        assert response['body'] == '"abc@x.y"'

    @mock_dynamodb2
    def test_subscribe(self):
        table_name = 'emailAddresses'
        dynamodb = boto3.resource('dynamodb', 'us-east-1')
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        event = {"pathParameters": {"email": "abc@x.y"}}

        response = subscribe(event, None)
        assert response['statusCode'] == 200
        assert response['body'] == '"abc@x.y"'
