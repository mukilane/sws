import io
import time

import requests

import picamera


class ImageRecognizer(object):
    def __init__(self):
        self.image_file = './test.jpg'

    def capture(self):
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                camera.start_preview()
                time.sleep(2)
                camera.capture(self.image_file)
                camera.stop_preview()
        except:
            print("Error in opening camera")

    def getCaption(self):
        result = requests.post(
            "https://api.deepai.org/api/densecap",
            files={
                'image': open(self.image_file, 'rb'),
            },
            headers={'api-key': '7bb8a18d-b8ee-48d8-a576-eebd38a9da5f'}
        )
        print(result.json())
    
    def 


if __name__ == "__main__":
    recognizer = ImageRecognizer()
    recognizer.capture()
    recognizer.getCaption()
