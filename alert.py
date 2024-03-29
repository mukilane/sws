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
    2. Push notificationsfire
"""

from time import sleep

import requests
import json
from twilio.rest import Client

from config_reader import config
from firebase_client import firebase
from gps import GPS

MAKER_BASE_URL = "https://maker.ifttt.com/trigger/"
EVENT = "send_sms"
AUTH_URL = "/with/key/" + config.get('keys', 'IFTTT_MAKER_KEY')
TWILIO_ACCOUNT_SID = config.get('keys', 'TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config.get('keys', 'TWILIO_AUTH_TOKEN')
CLOUD_FUNCTION_ENDPOINT = config.get('GOOGLE', 'CLOUD_FUNCTION_ENDPOINT')


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

    def alert(self):
        """Starts a logging session and sends SMS and push notification

        Logs the location of the user into the Firestore until exit. The 
        time interval between the logs is 10 seconds
        """
        self.sendSMS("I am in emergency")
        self.sendPushNotification()
        # For Demo
        self.gps_spoof()

        # Actual code
        # firebase.newSession()
        # while True:
        #     firebase.log(self.gps.getPosition())
        #     sleep(10)

    def gps_spoof(self):
        """Spoofs the GPS coordinates for demo
        """
        print("Logging Location")
        firebase.newSession()
        positions = json.load(open('gps_spoof.json'))
        for pos in positions['locations']:
            firebase.log(pos)
            sleep(2)

    def sendPushNotification(self):
        """Sends a push notification to the Tracker users

        Arguments:
            message {dict} -- dict containing location
        """
        print("Sending Push Notification")
        location = json.dumps(firebase.getPosition())
        payload = {"notification": {
            "title": "Person in Emergency", "body": location}}
        try:
            requests.post(CLOUD_FUNCTION_ENDPOINT, json=payload, timeout=1)
        except requests.exceptions.ReadTimeout:
            print("Error in sending the push notification")

    def sendSMS_IFTTT(self, message):
        """Sends a POST request to IFTTT Maker service

        Arguments:
            message {dict} -- dict containing three values

        Returns:
            Response -- response text from IFTTT
        """
        self.payload = message
        self.url = MAKER_BASE_URL + EVENT + AUTH_URL
        return requests.post(self.url, self.payload)

    def sendSMS(self, message):
        """Sends SMS using the Twilio API

        Initiates a Twilio client with the Account SID and Auth Token
        The 'from' number is a registered Twilio number associated with
        the account. The 'to' number is the recipent number which has to 
        be verified with Twilio for Trial accounts.

        A prefix string will be attached by Twilio in the message body for
        Trial accounts.

        Arguments:
            message {string} -- The message to be sent
        """

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        try:
            result = client.messages.create(
                from_="+16182059188",
                to="+919962473577",
                body=message
            )
        except:
            print("Error sending SMS with Twilio")


if __name__ == "__main__":
    alerter = Alerter()
    # alerter.sendSMS("Hello")
    alerter.alert()
    # alerter.sendPushNotification()
    # alerter.gps_spoof()
