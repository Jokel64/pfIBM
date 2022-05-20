from enum import Enum
import logging as lg
import os

global_gateway_mode = os.getenv("pfIBM-mode")


class GatewayStatus(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class ErrorCodes(Enum):
    SUCCESS = 0
    GENERAL_ERROR = 1
    DEVICE_NOT_CONNECTED = 2


class Gateway:
    def __init__(self):
        self.status = GatewayStatus.ONLINE
        self.name = "Undefined"

    def init_physical_gateway(self):
        lg.error(f"{self} has not overridden the init_physical_gateway function yet!")

    def delegate_to_physical_device(self, value, **kwargs):
        lg.error(f"{self} has not overridden the delegate_to_device function yet or uploads are not supported!")
        return 0

    def delegate_from_physical_device(self, **kwargs):
        lg.error(f"{self} has not overridden the delegate_from_device function yet or downloads are not supported!")
        return -1
