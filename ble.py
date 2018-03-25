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
"""Bluetooth Module

This module implements methods to start, stop, manage the bluetooth service
and facilitates advertising and scanning of Beacons.
"""
import json
from time import sleep
from tts import speak
from bleson import get_provider, Observer
#from beacontools import BeaconScanner, EddystoneFilter, EddystoneTLMFrame


#def callback(bt_addr, rssi, packet, additional_info):
#    """Callback for when message arrives
#
#    Arguments:
#        bt_addr {[type]} -- [description]
#        rssi {[type]} -- [description]
#        packet {[type]} -- [description]
#        additional_info {[type]} -- [description]
#    """
#    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))


class BLE(object):

    def __init__(self):
        self.adapter = get_provider().get_adapter()
        self.observer = Observer(self.adapter)
        self.observer.on_advertising_data = self.onData

    def onData(self, data):
        result = data.name.strip()[1:]
        print(result)
        speak(result)

    def start(self):
        self.observer.start()
        sleep(2)
        self.observer.stop()

    def scan(self):
        """Scans for beacons"""

        self.scanner.start()
        sleep(10)
        self.scanner.stop()


if __name__ == "__main__":
    ble = BLE()
    ble.start()
