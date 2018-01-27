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


from configparser import SafeConfigParser

import assist
from alert import Alerter
from gps import GPS
from hardware import Hardware
from maps import Maps

config = SafeConfigParser()
config.read('config.ini')


class SANAS(object):

    def __init__(self):
        self.assistant = assist
        self.gps = GPS()
        self.maps = Maps()
        self.hardware = Hardware()
        self.alerter = Alerter()
        try:
            self.hardware.setup(self.alert, self.navigate, self.assist)

    def start(self):
        """Starts the conversation"""

    def stop(self):
        """Stops the conversation"""

    def assist(self, channel):
        """Calls the assist stream"""
        self.assistant.main()

    def navigate(self, channel):
        """Calls the navigation stream"""
        self.maps.startNavigation()

    def alert(self, channel):
        """Calls the alert steam

        Arguments:
            channel {[type]} -- [description]
        """
        self.alerter.sendSMS()
