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

"""Hardware Module

This modules implements methods to interface with the hardware (Raspberry Pi).
"""

import Rpi.GPIO as GPIO
import time
import serial

GPIO_ALERT_PIN = 24
GPIO_ASSISTANT_PIN = 22
GPIO_NAVIGATE_PIN = 20
GPIO_CLASSIFIER_PIN = 19
GPIO_RANGER_PIN = 28


class Hardware(object):

    def __init__(self):
        self.available = False

    def setup(self, alert, navigate, assist):
        """Sets up all the GPIO pins and callbacks
        
        Arguments:
            alert {func} -- Callback to alert 
            navigate {func} -- Callback to start navigation
            assist {func} -- Callback to start the assistant
        """
        # GPIO set to BCM mode
        GPIO.setMode(GPIO.BCM)
        # Pin Setup
        GPIO.setup(GPIO_ALERT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_ASSISTANT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_NAVIGATE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Callbacks
        # Boucetime is set to debounce the button presses   
        GPIO.add_event_detect(GPIO_ALERT_PIN, GPIO.FALLING,
                              callback=alert, bouncetime=300)
        GPIO.add_event_detect(GPIO_ASSISTANT_PIN, GPIO.FALLING,
                              callback=assist, bouncetime=300)
        GPIO.add_event_detect(GPIO_NAVIGATE_PIN, GPIO.FALLING,
                              callback=navigate, bouncetime=300)
        self.available = True

    def cleanup(self):
        """Cleans up all the ports used"""
        GPIO.cleanup()
    
    def ranger(self):
        """Reads ultrasonic sensor data
        
        Connects to Arduino through I2C and receives data from the 
        ultrasonic sensor.
        This function will run in a separate thread.
        """
        try:
            port = serial.Serial('dev/ttyUSB0', 9600)
        except:
            print("Connection error")
            exit()
        while True:
            val = port.readline()
            # Notify based on 
