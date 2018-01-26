# Main File
# This invokes all the modules

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
