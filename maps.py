import re
from datetime import datetime
import dialogflow
import googlemaps
import gps

GOOGLE_MAPS_API_KEY = 'AIzaSyAZbBobi42KFDDcAX8OMew5IKzWnyjCQ88'


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
