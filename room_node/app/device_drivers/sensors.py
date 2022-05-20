from .prototypes import Device, DeviceTypes


class Climate(Device):
    def __init__(self, **kwargs):
        super().__init__(DeviceTypes.SENSORS, **kwargs)

    def __str__(self):
        return self.name

    def get_state(self):
        state = self.gateway.delegate_from_physical_device()
        return state


class Lighting(Device):
    def __init__(self, **kwargs):
        super().__init__(DeviceTypes.SENSORS, **kwargs)

    def get_state(self):
        state = self.gateway.delegate_from_physical_device()
        return state

