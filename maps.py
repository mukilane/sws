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
from datetime import datetime

import dialogflow
import googlemaps

import gps
from config_reader import config
from tts import speak

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

    def strip_tags(self, html):
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
            #         print(self.strip_tags(step["html_instructions"]))
            print(self.directions)
        except:
            print("Error occured while getting diretions")

    def isDestinationReached(self):
        """Check if the destination is reached"""

    def getCurrentLocation(self):
        """Rerieves the current location

        Uses GPS if available, eles uses Geolocation.
        """
        if self.gps.available:
            self.currentLocation = self.gps.getPosition()
        else:
            data = self.maps.geolocate()['location']
            self.currentLocation['lat'] = data['lat']
            self.currentLocation['lng'] = data['lng']
            
            # For Demo
            self.currentLocation['lat'] = 12.8008838
            self.currentLocation['lng'] = 80.22403039999999
            
        return self.currentLocation

    def getNearby(self, type):
        """Gets the nearby places 

        Returns:
            dict -- An array of dict containing places
        """
        places = []
        location = self.getCurrentLocation()
        result = self.maps.places_nearby(
            location=location,
            radius=100,
            type=type
        )['results']
        for r in result:
            places.append(r['name'])
        print(places)
        # speak(result)
        return result

    def getBearing(self):
        """Gets the current place of the user in a human readable form

        Returns:
            Place -- contains long_name, short_name 
        """
        location = self.getCurrentLocation()
        result = self.maps.reverse_geocode(
            location
        )[2]['formatted_address']
        print(result)
        speak(result)
        return result

    def startNavigation(self, source, destination):
        for step in self.directions[0]['legs']:
            speak(step)
            print(step)

    def getBusRoute(self, destination):
        """Retrieves the bus routes from source to destination"""
        result = self.maps.directions(
            origin=self.getCurrentLocation(),
            destination="K.K.Nagar",
            mode="transit",
            transit_mode="bus"
        )
        steps = []
        buses = []
        busStr = ""
        for r in result[0]['legs'][0]['steps']:
            steps.append(r['html_instructions'])
            if r['travel_mode'] == "TRANSIT":
                bus = r['transit_details']['line']['short_name']
                buses.append(bus)
                busStr = busStr + " " + bus
        speak("Available buses are" + busStr)
        for step in steps:
            speak(step)
        print(steps, buses)


if __name__ == "__main__":
    maps = Maps()
    # maps.getDirections('ashok pillar', 'tambaram', 'walking')
    # maps.getBusRoute("ashok pillar")
    # maps.getBearing()
    print(maps.getNearby("hospital"))
