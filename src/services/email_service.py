import boto3
from botocore.exceptions import ClientError

client = boto3.client('ses', region_name="us-east-1")

class EmailService:
    SENDER = "Sender Name <terrazoon@gmail.com>"
    RECIPIENT = "razorfangius@yahoo.com"
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
        print(f"EmailService._get_html {quote} {my_html}")
        return my_html

    @staticmethod
    def send_email(quote):
        print(f"EmailService.send_mail receives {quote}")
        my_html = EmailService._get_html(quote)
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        EmailService.RECIPIENT,
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
                Source=EmailService.SENDER
            )

        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
