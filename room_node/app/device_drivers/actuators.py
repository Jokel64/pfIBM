from .prototypes import Device, DeviceTypes
import logging as lg


# Helper classes
class HVACState:
    class VentilationStrength:
        OFF = 0
        L1 = 1
        L2 = 2
        MAX = 3

    def __init__(self, temperature: float, humidity: float, ventilation_strength: VentilationStrength):
        self.temperature = temperature
        self.humidity = humidity
        self.ventilation_strength = ventilation_strength


# Main classes
class Lamp(Device):
    def __init__(self, **kwargs):
        super().__init__(DeviceTypes.ACTUATORS, **kwargs)
        self.state = None
        self.brightness = 0                                                             # 0...1
        self.dimmable = False
        if "class" in kwargs and "dimmable" in kwargs["class"]:
            self.dimmable = True

        if "addr" in kwargs:
            self.addr = kwargs["addr"]
        else:
            lg.error("A Lamp needs an address!")
            exit(1)

    def __str__(self):
        return self.name

    def set_state(self, new_val):
        if new_val > 1 or new_val < 0:
            lg.error("Brightness set out of bounds!")
            return

        if not self.dimmable and new_val not in [0, 1]:
            lg.error(f"{str(self)} is not dimmable but received a float value!")
            return

        if self.gateway.delegate_to_physical_device(new_val, addr=self.addr) == 0:
            self.state = new_val
        else:
            self.state = None


class PowerSocket(Device):
    def __init__(self, **kwargs):
        super().__init__(DeviceTypes.ACTUATORS, **kwargs)
        self.state = None

    def __str__(self):
        return self.name

    def set_state(self, new_state: bool):
        if type(new_state) != bool:
            lg.error("Power socket can only have boolean states")
            return
        if self.gateway.delegate_to_physical_device(new_state) == 0:
            self.state = new_state
        else:
            self.state = None


class HVAC(Device):
    def __init__(self, **kwargs):
        super().__init__(DeviceTypes.ACTUATORS, **kwargs)
        self.state = None

    def __str__(self):
        return self.name

    def set_state(self, new_state: HVACState):
        if type(new_state) != HVACState:
            lg.error("HVACs can only have HVAC-states")
            return
        if self.gateway.delegate_to_physical_device(new_state) == 0:
            self.state = new_state
        else:
            self.state = None


class Blinds(Device):
    def __init__(self, **kwargs):
        super().__init__(DeviceTypes.ACTUATORS, **kwargs)
        self.state = None

    def __str__(self):
        return self.name

    def set_state(self, new_val):
        if new_val > 1 or new_val < 0:
            lg.error("Blinds level set out of bounds!")
            return

        if self.gateway.delegate_to_physical_device(new_val) == 0:
            self.state = new_val
        else:
            self.state = None
