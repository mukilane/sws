import re
from datetime import datetime

import dialogflow
import googlemaps


def detect_intent_texts(session_id, texts):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""

    project_id = "project-harmony" 
    language_code = "en"
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))


# Hard code the Home location
currentPosition = { 'lat': 0, 'lng': 0 }

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

if __name__ == "__main__":
    getCurrentLocation()
    print(currentPosition)
