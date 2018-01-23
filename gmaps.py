import re
from datetime import datetime

import dialogflow
import googlemaps

import gps

GOOGLE_MAPS_API_KEY = 'AIzaSyAZbBobi42KFDDcAX8OMew5IKzWnyjCQ88'

def strip_tags(html):
    return re.sub('<[^<]+?>', '', html)

gmaps = googlemaps.Client(key='AIzaSyAZbBobi42KFDDcAX8OMew5IKzWnyjCQ88')

def getDirections(source, dest, mode, dept_time):
    '''Obtains the directions between the given points'''

    if not dept_time:
        dept_time = datetime.now()

    directions = gmaps.directions(
        source,
        dest,
        mode=mode,
        departure_time=dept_time)
    
    legs = data[0]["legs"]
    
    for leg in legs:
        for step in leg["steps"]:
            print(strip_tags(step["html_instructions"]))


def checkProgress():
    '''Checks the progress of the user'''

def isDestinationReached():
    '''Checks whether the destination is reached'''

def getCurrentLocation(gps=False):
    '''Determines the current location of the user using either GPS or Geolocation'''
    if gps:
        # Logic to get data from GPS
        print(1)
    else:
        data = gmaps.geolocate()["location"]
        currentPosition['lat'] = data["lat"]
        currentPosition['lng'] = data["lng"]


class Maps(object):
    """This class will initiate a map session and provides directions"""

    def __init__(self):
        self.maps = None
        self.currentLocation = { 'lat': 0.0, 'lng': 0.0 }
        self.destination = None
        self.transit_mode = None
        self.directions = None
        self.steps = None
        try:
            self.maps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        except:
            print("Error occured during Maps Initialization")
    
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
            print(self.directions)
        except:
            print("Error occured while getting diretions")
    
    def isDestinationReached():
        """Check if the destination is reached"""

    def getCurrentLocation():
        """Get the current location"""
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
