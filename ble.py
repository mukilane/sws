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

from beacontools import BeaconScanner, EddystoneFilter, EddystoneTLMFrame


def callback(bt_addr, rssi, packet, additional_info):
    """Callback for when message arrives

    Arguments:
        bt_addr {[type]} -- [description]
        rssi {[type]} -- [description]
        packet {[type]} -- [description]
        additional_info {[type]} -- [description]
    """
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))


class BLE(object):

    def __init__(self):
        self.scanner = BeaconScanner(
            callback,
            packet_filter=EddystoneTLMFrame
        )
        self.mockdata = json.load(open('mock.json'))

    def start(self):
        self.service.start_advertising("11111111-2222-3333-4444-555555555555",
                                       1, 1, 1, 200)
        self.service.stop_advertising()

    def scan(self):
        """Scans for beacons"""

        self.scanner.start()
        sleep(10)
        self.scanner.stop()


if __name__ == "__main__":
    ble = BLE()
    ble.scan()
