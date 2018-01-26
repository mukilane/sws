#Used to interface the buttons
import Rpi.GPIO as GPIO
import time

GPIO_ALERT_PIN = 24
GPIO_ASSISTANT_PIN = 22
GPIO_NAVIGATE_PIN = 20
GPIO_CLASSIFIER_PIN = 19

class Hardware(object):
    
    def __init__(self):
        pass

    def setup(self, alert, navigate, assist):
        GPIO.setMode(GPIO.BCM)
        GPIO.setup(GPIO_ALERT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_ASSISTANT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        GPIO.add_event_detect(GPIO_ALERT_PIN, GPIO.FALLING, callback=alert, bouncetime=300)
        GPIO.add_event_detect(GPIO_ASSISTANT_PIN, GPIO.FALLING, callback=assist, bouncetime=300)
        GPIO.add_event_detect(GPIO_NAVIGATE_PIN, GPIO.FALLING, callback=navigate, bouncetime=300)
