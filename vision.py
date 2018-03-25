import io
import os
import time
import google.cloud.vision
import picamera
import requests

def TakePic():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(2)
        camera.capture('./test.jpg')
        camera.stop_preview()

#vision_client = google.cloud.vision.ImageAnnotatorClient()

#with io.open('./test.jpg', 'rb') as image_file:
    #content = image_file.read()

#image = google.cloud.vision.types.Image(content=content)
#response = vision_client.label_detection(image=image)

#for label in response.label_annotations:
#    print(label.description)

def DeepAi():
    r = requests.post(
      "https://api.deepai.org/api/densecap",
      files={
        'image': open('./test.jpg', 'rb'),
      },
      headers={'api-key' : '7bb8a18d-b8ee-48d8-a576-eebd38a9da5f'}
    )
    print(r.json())

TakePic()
DeepAi()
