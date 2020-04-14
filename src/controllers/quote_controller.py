import json
from random import randrange

# import requests


# def chuck_norris_joke(event, context):
#
#     joke_response = requests.get("http://api.icndb.com/jokes/random")
#     joke_as_dict = json.loads(joke_response.text)
#     joke = joke_as_dict["value"]["joke"]
#     print(f"Here's a joke: {joke}")
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(joke)
#     }
#     return response

def stoic_quote(event, context):
    with open('stoic_quotes.json') as f:
        data = json.load(f)
    quote_list = data["Quotes"]
    num_quotes = len(quote_list)
    myrand = randrange(num_quotes)
    quote = quote_list[myrand]
    print(f"Author: {quote['Author']} Quote: {quote['Quote']}")
    response = {
        "statusCode": 200,
        "body": json.dumps(quote)
    }
    return response