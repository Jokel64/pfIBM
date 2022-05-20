from .prototypes import Gateway, global_gateway_mode, ErrorCodes
import logging as lg


class PfSim(Gateway):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "pfIBM Simulation"
        self.init_physical_gateway()

    def init_physical_gateway(self):
        if global_gateway_mode == "production":
            # todo phillips gateway
            lg.error("pfIBM-sim Gateway init not yet implemented.")
        # development mode
        else:
            self.connected_devices = {
                0xb1: 0,
                0xb2: 0,
                0xb3: 0
            }

    def delegate_to_physical_device(self, value, **kwargs):
        if "addr" not in kwargs:
            lg.error("field 'addr' needed for download delegate!")
            return ErrorCodes.GENERAL_ERROR
        addr = kwargs["addr"]

        if addr not in self.connected_devices:
            lg.error(f"Device {addr} not connected to gateway.")
            return ErrorCodes.DEVICE_NOT_CONNECTED

        lg.debug(f"pfIBM-sim is writing {value} to device at {addr}.")
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
