from .prototypes import Gateway, global_gateway_mode, ErrorCodes
import logging as lg
from phue import Bridge


class PhillipsHueGateway(Gateway):
    def __init__(self, **kwargs):
        self.bridge = None
        self.ip = kwargs["ip"]
        super().__init__()
        self.name = "Phillips Hue"
        self.init_physical_gateway()
        #self.bridge = None # WISOOOOOOOO ??????
        self.last_values = dict()
        self.error = False

    def init_physical_gateway(self):
        try:
            self.bridge = Bridge(self.ip)
            self.bridge.connect()
        except Exception as e:
            lg.error(f"Couldnt connect to PHUE: {e}")
            self.error = True

    def delegate_to_physical_device(self, value, **kwargs):
        if "addr" not in kwargs:
            lg.error("field 'addr' needed for 'to' delegate [PhillipsHue]!")
            return ErrorCodes.GENERAL_ERROR

        addr = int(kwargs["addr"])
        print(f"HUE - setting {addr} to {value}")
        if self.bridge is not None and not self.error:

            self.bridge.set_light(addr,'on', True)
            self.bridge.set_light(addr, 'bri', int(value * 255))
            self.last_values[addr] = value

        return ErrorCodes.SUCCESS

    def delegate_from_physical_device(self, **kwargs):
        if "addr" not in kwargs:
            lg.error("field 'addr' needed for 'from' delegate []!")
            return

        return self.last_values[kwargs['addr']]

    def get_bridge_state(self):
        return self.bridge.get_api()