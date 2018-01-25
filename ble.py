from bluetooth.ble import BeaconService

class BLE(object):
    
    def __init__(self):
        self.service =  BeaconService()
    
    def start(self):
        self.service.start_advertising("11111111-2222-3333-4444-555555555555",
            1, 1, 1, 200)
        self.service.stop_advertising()

    def scan(self):
        pass
