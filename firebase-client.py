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

import firebase_admin
from firebase_admin import credentials, firestore
from configparser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

FIREBASE_SERVICE_ACCOUNT_CREDENTIALS = config.get('firebase', 'FIREBASE_SERVICE_ACCOUNT')
FIREBASE_DATABASE_URL = config.get('firebase', 'FIREBASE_DATABASE_URL')

class Firebase(object):

    def __init__(self):
        self.credentials = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_CREDENTIALS)
        self.client = None
        self.ref = None
        try:
            firebase_admin.initialize_app(self.credential, {
                'databaseURL': FIREBASE_DATABASE_URL
            })
            self.client = firestore.client()
            self.ref = self.client.document('users/cJZRuTCZR4yL4za3OfMM')

    def getPosition(self):
        self.data = self.ref.get()
        self.position = self.data.to_dict()['lastLocation']
    
    def log(self, data):
        pass
