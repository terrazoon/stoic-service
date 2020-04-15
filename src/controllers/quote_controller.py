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
from src.services.email_service import EmailService


def _get_image(image_data):

    image = f"<div><image src='{image_data}' alt='image'</div>"
    return image

def stoic_quote(event, context):
    with open('stoic_quotes.json') as f:
        data = json.load(f)
    quote_list = data["Quotes"]
    num_quotes = len(quote_list)
    myrand = randrange(num_quotes)
    quote = quote_list[myrand]
    print(f"Author: {quote['Author']} Quote: {quote['Quote']}")

    # with open('images.json') as f:
    #     images = json.load(f)
    #
    # myhtml = "<html><body><h2>" + quote['Quote'] + "/h2" + "<br/><br/>" + quote['Author']
    # # myhtml += _get_image(images[quote['Author']])
    # myhtml += "</body></html>"
    #
    # print(myhtml)
    print(f"about to send email from controller with {quote}")
    EmailService.send_email(quote)

    response = {
        "statusCode": 200,
        "body": json.dumps(quote)
    }
    return response