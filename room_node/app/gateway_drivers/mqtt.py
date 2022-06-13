from .prototypes import Gateway


class MQTTGateway(Gateway):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "MQTT Gateway"
        self.init_physical_gateway()

    def init_physical_gateway(self):
        pass

    def delegate_to_physical_device(self, value, **kwargs):
        pass

    def delegate_from_physical_device(self, **kwargs):
        pass
