import io
import time

import requests

import picamera
from tts import speak

# import hardware

class ImageRecognizer(object):
    def __init__(self):
        self.hardware = None
        self.image_file = './test.jpg'
    
    def setup(self):
        self.hardware = hardware.Hardware()
        self.hardware.setupRecognizer(self.getDescription)

    def capture(self):
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                camera.start_preview()
                time.sleep(2)
                camera.capture(self.image_file, use_video_port=True)
                camera.stop_preview()
        except:
            print("Error in opening camera")

    def getCaption(self):
        self.capture()
        print("Captured")
        result = requests.post(
            "https://api.deepai.org/api/densecap",
            files={
                'image': open(self.image_file, 'rb'),
            },
            headers={'api-key': '<enter-your-api-key>'}
        )
        caption = result.json()['output']['captions'][0]['caption']
        speak(caption)
        # print(result.json())

    def getDescription(self):
        self.capture()
        print("Captured")
        result = requests.post(
            "https://api.deepai.org/api/neuraltalk",
            files={
                'image': open(self.image_file, 'rb'),
            },
            headers={'api-key': '<enter-your-api-key>'}
        )
        res = result.json()['output']
        # print(result.json())
        speak(res)


if __name__ == "__main__":
    recognizer = ImageRecognizer()
    # recognizer.getCaption()
    while True:
        pass
