# Main File
# This invokes all the modules

import gps
import maps
import alert


class SANAS(object):

    def __init__(self):
        self.gps = gps.GPS()
        self.maps = maps.Maps()

    def start(self):
        """Starts the conversation"""

    def stop(self):
        """Stops the conversation

        """

    def alert(self):
