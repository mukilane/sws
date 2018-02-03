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

"""GPS Module

This module implements methods to retrieve GPS coordinates from the sensor
and/or from Firestore.
"""

from config_reader import config
from firebase_client import firebase


class GPS(object):
    """Wrapper for GPS sensor."""

    def __init__(self):
        # Whether GPS sensor is available
        self.available = False

    def getPosition(self):
        """Retrieves the location data from the GPS module

        Currently, uses Firebase to mock GPS data

        Returns:
            dict -- Contains lat/lng
        """
        if not self.available:
            location = firebase.getPosition()
            return location


if __name__ == "__main__":
    gps = GPS()
    print(gps.getPosition())
