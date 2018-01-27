# Copyright (C) 2018 Mukil Elango
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Alert Module 

This module implements methods for alerting the user's preset contact/contacts
through IFTTT or Twilio.

This module also implements methods for logging the user's location data when
an emergency session is invoked. The location is logged in a Firebase Firestore
database.

Todo:
    1. Add more methods and error checking
"""

import requests
from gps import GPS
from twilio.rest import Client
from configparser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')
MAKER_BASE_URL = "https://maker.ifttt.com/trigger/"
EVENT = "send_sms"
AUTH_URL = "/with/key/" + config.get('keys', 'IFTTT_MAKER_KEY')
TWILIO_ACCOUNT_SID = config.get('keys', 'TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config.get('keys', 'TWILIO_AUTH_TOKEN')

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
        self.gps = GPS()

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

    def 


if __name__ == "__main__":
    alerter = Alerter()
    alerter.sendSMS()
