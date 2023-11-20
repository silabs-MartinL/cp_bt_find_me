# Import library modules
from adafruit_ble.services import Service
from adafruit_ble.uuid import StandardUUID
from adafruit_ble.attributes import Attribute
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.characteristics.int import Uint8Characteristic

class ImmediateAlertService(Service):
    uuid = StandardUUID(0x1802)

    alert_level = Uint8Characteristic(
        uuid = StandardUUID(0x2A06),
        properties = (Characteristic.READ | Characteristic.WRITE_NO_RESPONSE)
    )

    def __init__(self, service=None):
        super().__init__(service=service)
        self.connectable = True