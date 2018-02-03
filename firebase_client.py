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

"""Firebase Module

This module implements methods to query and log data in the Firebase Firestore
using the Firebase Admin SDK and Google Cloud Firestore SDK.

Firebase Admin SDK Documentation:
https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/
"""

import datetime

import firebase_admin
from firebase_admin import credentials, firestore

from config_reader import config

FIREBASE_SERVICE_ACCOUNT_CREDENTIALS = config.get(
    'firebase', 'FIREBASE_SERVICE_ACCOUNT')
FIREBASE_DATABASE_URL = config.get('firebase', 'FIREBASE_DATABASE_URL')
FIREBASE_USER_ID = config.get('firebase', 'FIREBASE_USER_ID')


class Firebase(object):
    """Helper to push/pull data from Firebase"""

    def __init__(self):
        """Initializes the Firebase Admin SDK

        A new session is created for logging the locations. Each user has a
        unique ID, referenced as FIREBASE_USER_ID which is the document ID.
        """
        self.credentials = credentials.Certificate(
            FIREBASE_SERVICE_ACCOUNT_CREDENTIALS)
        self.client = None
        self.document = None
        self.session = []
        try:
            firebase_admin.initialize_app(self.credentials, {
                'databaseURL': FIREBASE_DATABASE_URL
            })
            self.client = firestore.client()
            self.document = self.client.document('users/' + FIREBASE_USER_ID)
        except:
            print("Error during Firebase initialization")
            exit()

    def newSession(self):
        """Initiates a new logging session"""
        self.session = []

    def getPosition(self):
        """Gets the last location

        The last location is stored as a Geopoint with a key 'lastLocation'

        Returns:
            location -- A dict with lat/lng
        """
        data = self.document.get()
        self.position = {
            'lat': data.to_dict()['lastLocation'].latitude,
            'lng': data.to_dict()['lastLocation'].longitude
        }
        return self.position
    
    def log(self, coord):
        """Logs the location and timestamp

        The locations are stored in session array and is reset for each 
        session. The built in SERVER_TIMESTAMP is used to order the logs
        chronologically for each session.

        Arguments:
            coord -- A dict with lat/lng
        """
        location = firestore.GeoPoint(coord['lat'], coord['lng'])
        instance = {
            'location': location,
            'timestamp': datetime.datetime.utcnow()
        }
        self.session.append(instance)
        update = {
            'lastLocation': location,
            'session': self.session,
            'lastUpdated': firestore.SERVER_TIMESTAMP
        }
        self.document.update(update)


# Single instance of Firebase shared between different submodules
# This will initiate a new session of logging
firebase = Firebase()
