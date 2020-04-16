import unittest

from src.controllers.quote_controller import stoic_quote


class QuoteControllerTest(unittest.TestCase):

    def test_stoic_quote(self):
        response = stoic_quote(None, None)
        assert response['statusCode'] == 200
        assert response['body'] == '"abc@x.y"'
