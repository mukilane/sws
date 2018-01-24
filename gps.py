#Receives GPS Coordinates from GPS module or a phone

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class GPS(object):
    
    def __init__(self):
        self.cred = credentials.Certificate('/home/mukil/Downloads/project-harmony-firebase-adminsdk-o8sr8-9fd814dc8d.json')
        self.client = None
        self.ref = None
        try:
            firebase_admin.initialize_app(self.cred, {
                'databaseURL' : 'https://project-harmony.firebaseio.com'
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