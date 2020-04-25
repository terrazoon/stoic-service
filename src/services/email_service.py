import boto3
from botocore.exceptions import ClientError

client = boto3.client('ses', region_name="us-east-1")

ssm = boto3.client('ssm')
parameter = ssm.get_parameter(Name='/StoicService/senderEmail', WithDecryption=True)
SENDER = parameter['Parameter']['Value']
SENDER = "Stoic Service <" + SENDER + ">"


class EmailService:
    AWS_REGION = "us-east-1"
    SUBJECT = "Stoic Quote of the Day"
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                 )

    CHARSET = "UTF-8"

    @staticmethod
    def _get_html(quote):
        my_html = f"<html><head></head><body><h2>{quote['Quote']}</h2><p>{quote['Author']}</p></body></html>"
        return my_html

    @staticmethod
    def send_email(quote, my_email_address):
        my_html = EmailService._get_html(quote)
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        my_email_address,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': EmailService.CHARSET,
                            'Data': my_html,
                        },
                        'Text': {
                            'Charset': EmailService.CHARSET,
                            'Data': EmailService.BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': EmailService.CHARSET,
                        'Data': EmailService.SUBJECT,
                    },
                },
                Source=SENDER
            )

        except ClientError as e:
            print(e.response['Error']['Message'])
