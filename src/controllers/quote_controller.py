import json
from random import randrange

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

    print(f"about to send email from controller with {quote}")
    EmailService.send_email(quote)

    response = {
        "statusCode": 200,
        "body": json.dumps(quote)
    }
    return response
