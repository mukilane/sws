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
"""

from configparser import SafeConfigParser

import assist
from alert import Alerter
from gps import GPS
#from hardware import Hardware
from maps import Maps

config = SafeConfigParser()
config.read('config.ini')


class SANAS(object):

    def __init__(self):
        self.assistant = assist
        self.gps = GPS()
        self.maps = Maps()
        #self.hardware = Hardware()
        self.alerter = Alerter()

        self.isAssistantRunning = False
        self.isAlertRunning = False
        self.isNavigationRunning = False

    def start(self):
        """Starts listening on the hardware"""
        try:
            pass
            # self.hardware.setup(self.alert, self.navigate, self.assist)
        except:
            print("Error during hardware setup")

    def stop(self):
        """Stop the hardware listening"""
        self.hardware.cleanup()

    def assist(self, channel):
        """Calls the assist stream"""
        if not self.isAssistantRunning:
            self.isAssistantRunning = True
            self.assistant.main()
            self.isAssistantRunning = False
        else:
            print("Action already running")

    def navigate(self, channel):
        """Calls the navigation stream"""
        if not self.isNavigationRunning:
            self.isNavigationRunning = True
            self.maps.startNavigation()
            self.isNavigationRunning = False
        else:
            print("Action already running")

    def alert(self, channel):
        """Calls the alert steam

        Arguments:
            channel {[type]} -- [description]
        """
        if not self.isAlertRunning:
            self.isAlertRunning = True
            self.alerter.sendSMS()
            self.isAlertRunning = False
        else:
            print("Action already running")

    def listen(self, channel):
        """Invokes the dialogflow agent"""
        

        

if __name__ == "__main__":
    sanas = SANAS()
    sanas.start()
