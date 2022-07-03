import json
import os
import boto3
import random


my_s3 = boto3.resource('s3')

my_bucket_name = os.environ["QUOTES_BUCKET_NAME"]


def get_quotes_from_s3(object_name):
    obj = my_s3.Object(my_bucket_name, object_name)
    body = obj.get()['Body'].read()
    body = json.loads(body)
    quotes = body['Quotes']
    return quotes


seneca_quotes = get_quotes_from_s3("quotes/seneca.json")
epictetus_quotes = get_quotes_from_s3("quotes/epictetus.json")
marcus_quotes = get_quotes_from_s3("quotes/marcus_aurelius.json")

#print(f"seneca quotes: {seneca_quotes}")


class QuotesService:

    @staticmethod
    def get_quote():
        quotes = QuotesService._pick_author()
        num = len(quotes)
        #print(f"found this many quotes {num}")
        my_rand = random.randint(0, num - 1)
        print(f"my rand {my_rand}")
        quote = quotes[my_rand]
        #print(f"returning quote {quote}")
        return quote

    @staticmethod
    def _pick_author():
        my_rand: str = random.choice(['seneca', 'epictetus', "marcus_aurelius"])
        if my_rand == 'seneca':
            return seneca_quotes
        elif my_rand == 'marcus_aurelius':
            return marcus_quotes
        else:
            return epictetus_quotes

