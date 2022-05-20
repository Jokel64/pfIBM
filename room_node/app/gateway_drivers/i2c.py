from .prototypes import Gateway, global_gateway_mode, ErrorCodes
import logging as lg


class I2cGateway(Gateway):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "I2C Gateway"
        self.init_physical_gateway()

    def init_physical_gateway(self):
        if global_gateway_mode == "production":
            # todo phillips gateway
            lg.error("I2C Gateway init not yet implemented.")
        # development mode
        else:
            self.connected_devices = {
                0xc1: 0,
                0xc2: 0,
                0xc3: 0
            }

    def delegate_to_physical_device(self, value, **kwargs):
        if "addr" not in kwargs:
            lg.error("field 'addr' needed for download delegate!")
            return ErrorCodes.GENERAL_ERROR
        addr = kwargs["addr"]
        if addr not in self.connected_devices:
            lg.error(f"Device {addr} not connected to gateway.")
            return ErrorCodes.DEVICE_NOT_CONNECTED

        lg.debug(f"I2C is writing {value} to device at {addr}.")
        self.connected_devices[addr] = value

        return ErrorCodes.SUCCESS

    def delegate_from_physical_device(self, **kwargs):
        if "addr" not in kwargs:
            lg.error("field 'addr' needed for download delegate!")
            return

        if kwargs["addr"] not in self.connected_devices:
            lg.error(f"Device {kwargs['addr']} not connected to gateway.")
            return ErrorCodes.DEVICE_NOT_CONNECTED

        return self.connected_devices[kwargs['addr']]
