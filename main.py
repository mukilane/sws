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
"""Main module


This module will import all the submodules and invoke them based on user 
selection.

The various operations are divided into streams/actions. Two or more streams 
can run in parallel. 
eg: Invoking assistant during navigation; Alerting during navigation
The various streams/actions are:
1. Navigate stream
    This invokes the maps module and starts a navigation or exploration
    session.
2. Assistant stream
    This invokes the Google Assistant module.
3. Alert stream
    This invokes the Alert module to send sms and log the location data.
"""

import threading

import pushassist1
from alert import Alerter
from config_reader import config
from dialogflowAssistant import DialogflowAssistant
from gps import GPS
from hardware import Hardware
from maps import Maps
from vision import ImageRecognizer


class SANAS(object):

    def __init__(self):
        self.assistant = pushassist1
        self.gps = GPS()
        self.maps = Maps()
        self.hardware = Hardware()
        self.alerter = Alerter()
        self.dialogflowAssistant = DialogflowAssistant()
        # self.assistThread = threading.Thread(target=self.assistant.main, args=(False, False))
        # self.assistThread.start()
        # self.assistThread.daemon = False
        self.recognizer = ImageRecognizer()
        self.SimpleAssistant = self.assistant.main(
            True, False)  # Returns a trigger function
        self.isAssistantRunning = False
        self.isAlertRunning = False
        self.isNavigationRunning = False

    def start(self):
        """Starts listening on the hardware"""
        try:
            pass
            self.hardware.setup(self.alert, self.listen, self.assist)
            self.hardware.setupRecognizer(self.recognizer.getDescription)
        except:
            print("Error during hardware setup")

    def stop(self):
        """Stop the hardware listening"""
        self.hardware.cleanup()

    def assist(self, channel):
        """Calls the assist stream"""
        if not self.isAssistantRunning:
            self.isAssistantRunning = True
            print("Starting Assistant")
            self.hardware.light(True)
            self.SimpleAssistant()
            self.hardware.light(False)
            print("Stopping Assistant")
            self.isAssistantRunning = False
        else:
            print("Assistant already running")

    def navigate(self, channel):
        """Calls the navigation stream"""
        if not self.isNavigationRunning:
            self.isNavigationRunning = True
            self.maps.startNavigation("home", "cape canevaral")
            self.isNavigationRunning = False
        else:
            print("Action already running")

    def alert(self, channel):
        """Calls the alert stream

        Arguments:
            channel {[type]} -- [description]
        """
        if not self.isAlertRunning:
            self.isAlertRunning = True
            self.alerter.alert()
            self.isAlertRunning = False
        else:
            print("Action already running")

    def listen(self, channel):
        """Invokes the dialogflow agent"""
        # self.assistant.main(True, True)
        print("Starting Dialogflow Assistant")
        response = self.dialogflowAssistant.detect()
        intent = response['intent']
        if intent == "Alert":
            self.alert(None)
        elif intent == "Navigate":
            self.navigate(None)
        elif intent == "ASSIST":
            self.assist(None)
        elif intent == "NEARBY":
            print(response['parameters']['place-type'])
            if "place-type" in response['parameters']:
                self.maps.getNearby(response['parameters']['place-type'])
            else:
                self.maps.getNearby("hospital")
        elif intent == "BEARING":
            self.maps.getBearing()
        elif intent == "BLE_BUS":
            self.maps.getBusRoute("home")


if __name__ == "__main__":
    sanas = SANAS()
    sanas.start()
    # sanas.listen("d")
    # sanas.assist('d')
    # sanas.listen("d")
    try:
        while True:
            pass
            # sanas.assist("d")
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        sanas.stop()
