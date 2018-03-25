import io
import os
import google.cloud.vision

vision_client = google.cloud.vision.ImageAnnotatorClient()

with io.open('./test.jpg', 'rb') as image_file:
    content = image_file.read()

image = google.cloud.vision.types.Image(content=content)
response = vision_client.label_detection(image=image)

for label in response.label_annotations:
    print(label.description)
