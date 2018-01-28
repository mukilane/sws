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
"""

import firebase_admin
from firebase_admin import credentials, firestore
from configparser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

FIREBASE_SERVICE_ACCOUNT_CREDENTIALS = config.get(
    'firebase', 'FIREBASE_SERVICE_ACCOUNT')
FIREBASE_DATABASE_URL = config.get('firebase', 'FIREBASE_DATABASE_URL')
FIREBASE_USER_ID = config.get('firebase', 'FIREBASE_USER_ID')

class Firebase(object):
    """Helper to push/pull data from Firebase"""

    def __init__(self):
        self.credentials = credentials.Certificate(
            FIREBASE_SERVICE_ACCOUNT_CREDENTIALS)
        self.client = None
        self.document = None
        self.ref = None
        try:
            firebase_admin.initialize_app(self.credentials, {
                'databaseURL': FIREBASE_DATABASE_URL
            })
            self.client = firestore.client()
            self.document = self.client.document('users/' + FIREBASE_USER_ID)
        except:
            print("Error during Firebase initialization")

    def getPosition(self):
        self.data = self.document.get()
        self.position = self.data.to_dict()
        return self.position

    def log(self, data):
        """Logs the location and timestamp
        
        Todo:
            Convert location to Geopoint using helpers.

        Arguments:
            data {dict} -- a dict containing lat/lng 
        """
        update = {
            'check': data,
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        self.document.update(update)

# Single instance of Firebase shared between different submodules
firebase = Firebase()