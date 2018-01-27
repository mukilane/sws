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

"""Maps Module

This module implements methods for navigation and discovery of surroundings.
Uses one of the following mapping service:
    1. Google Maps
    2. Mapbox
    3. OpenStreetMap

This module depends on the GPS module to get the current location and also 
actively track the position of the user along the path to offer turn-by-turn
directions.

Todo:
    1. Improve the navigation flow
    2. Support for OpenStreetMap
"""
import re
from configparser import SafeConfigParser
from datetime import datetime

import dialogflow
import googlemaps

import gps

config = SafeConfigParser()
config.read('config.ini')
GOOGLE_MAPS_API_KEY = config.get('keys', 'GOOGLE_MAPS_API_KEY')


class Maps(object):
    """This class will initiate a map session and provides directions"""

    def __init__(self):
        self.maps = None
        self.currentLocation = {'lat': 0.0, 'lng': 0.0}
        self.destination = None
        self.transit_mode = None
        self.directions = None
        self.steps = None
        self.gps = gps.GPS()
        try:
            self.maps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        except:
            print("Error occured during Maps Initialization")

    def strip_tags(html):
        return re.sub('<[^<]+?>', '', html)

    def getDirections(self, source, destination, mode):
        """Obtains the directions for a route"""

        departure_time = datetime.now()

        try:
            self.directions = self.maps.directions(
                source,
                destination,
                mode=mode,
                departure_time=departure_time
            )
            self.steps = self.directions[0]['legs'][0]['steps']
            # for leg in legs:
            #     for step in leg["steps"]:
            #         print(strip_tags(step["html_instructions"]))
            print(self.directions)
        except:
            print("Error occured while getting diretions")

    def isDestinationReached():
        """Check if the destination is reached"""

    def getCurrentLocation():

        if gps.available:
            self.currentLocation = gps.getLocation()
        else:
            data = self.maps.geolocate()['location']
            self.currentLocation['lat'] = data['lat']
            self.currentLocation['lng'] = data['lng']

    def startNavigation(self, source, destination):
        for step in self.directions[0]['legs']:
            print(step)


if __name__ == "__main__":
    maps = Maps()
    maps.getDirections('ashok pillar', 'tambaram', 'walking')
