from enum import Enum
import logging as lg

class Device:
    def __init__(self, device_type, gateway_ref, name="Undefined",  **kwargs):
        self.name = name
        self.device_type = device_type
        self.gateway = gateway_ref
        self.state = None

    def set_state(self, new_val):
        lg.error(f"{self.name} has no valid implementation of set_state!")

class DeviceTypes(Enum):
    SENSORS = "SENSORS"
    ACTUATORS = "ACTUATORS"
