#Receives GPS Coordinates from GPS module or a phone

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from configparser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

FIREABSE_SERVICE_ACCOUNT_CREDENTIALS = config.get('firebase', 'FIREBASE_SERVICE_ACCOUNT')
FIREBASE_DATABASE_URL = config.get('firebase', 'FIREBASE_DATABASE_URL')

class GPS(object):
    
    def __init__(self):
        self.cred = credentials.Certificate(FIREABSE_SERVICE_ACCOUNT_CREDENTIALS)
        self.client = None
        self.ref = None
        try:
            firebase_admin.initialize_app(self.cred, {
                'databaseURL' : FIREBASE_DATABASE_URL
            })
            self.client = firestore.client()
            self.ref = self.client.document('users/cJZRuTCZR4yL4za3OfMM')
            self.data = self.ref.get()
            self.position = self.data.to_dict()['lastLocation']
        except:
            print("Error during firebase app initialization")
    
    def sync(self):
        self.data = self.ref.get()
        self.position = self.data.to_dict()['lastLocation']

    def getPosition(self):
        self.sync()
        return self.position
    
if __name__ == "__main__":
    gps = GPS()
    gps.getPosition()