import requests
from twilio.rest import Client

MAKER_BASE_URL = "https://maker.ifttt.com/trigger/"
EVENT = "send_sms"
AUTH_URL = "/with/key/cfSecjPrUxCqVzEB9mqi4x"
TWILIO_ACCOUNT_SID = "AC4e27168210d1a16d51881f76a0e07fd8"
TWILIO_AUTH_TOKEN = "48af015ecfd97addaba5caab7e64728a"


class Alerter(object):
    """Performs requests to IFTTT Maker Service to send sms
    to the desired contact
    """

    def __init__(self):
        self.payload = {
            "value1": "",
            "value2": "",
            "value3": ""
        }
        self.url = ""

    def alert(self, payload):
        """Sends a POST request to IFTTT Maker service

        Arguments:
            payload {[dict]} -- [dict containing three values]

        Returns:
            [Response] -- [response text from IFTTT]
        """
        self.payload = payload
        self.url = MAKER_BASE_URL + EVENT + AUTH_URL
        return requests.post(self.url, self.payload)

    def sendSMS(self):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_="+16182059188",
            to="+919962473577",
            body="hello world"
        )


if __name__ == "__main__":
    alerter = Alerter()
    alerter.sendSMS()
