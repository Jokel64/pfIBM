from .prototypes import Actuator, Sensor
import logging as lg


# Helper classes
class HVACState:
    def __init__(self, temperature: float, ventilation_strength: float):
        self.temperature = temperature
        self.ventilation_strength = ventilation_strength


# Main classes
class Lamp(Actuator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dimmable = False
        if "class" in kwargs and "dimmable" in kwargs["class"]:
            self.dimmable = True

        self.max_mean_lux = 0
        if "max_mean_lux" in kwargs:
            self.max_mean_lux = int(kwargs["max_mean_lux"])
        else:
            lg.warning(f"Lamp {self.name} has no lux specified. Defaulting to 0...")

        if "addr" in kwargs:
            self.addr = kwargs["addr"]
        else:
            lg.error("A Lamp needs an address!")
            exit(1)

    def propose(self, new_val):
        if new_val > 1 or new_val < 0:
            lg.error("Brightness set out of bounds!")
            return 1

        if not self.dimmable and new_val not in [0, 1]:
            lg.error(f"{str(self)} is not dimmable but received a float value!")
            return 1

        self.proposed_state = new_val
        return 0

    def commit(self):
        if self.gateway.delegate_to_physical_device(self.proposed_state, **{"addr":self.addr}) == 0:
            self.last_state = self.proposed_state
            return 0
        else:
            self.last_state = None
            return 1


class PowerSocket(Actuator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def propose(self, new_state: bool):
        if type(new_state) != bool:
            lg.error("Power socket can only have boolean states")
            return 1
        self.proposed_state = new_state
        return 0


class HVAC(Actuator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.propose([20, 0])

    # value 0: temperature, value 1: intensity
    def propose(self, new_state):
        if len(new_state) != 2:
            lg.error("HVAC needs 2 states")
            return 1
        self.proposed_state = new_state
        return 0

    def get_current_proposed_watts(self):
        return self.max_watts * self.proposed_state[1]


class WindowBlinds(Actuator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def propose(self, new_val):
        if new_val > 1 or new_val < 0:
            lg.error("Blinds level set out of bounds!")
            return 1
        self.proposed_state = new_val
        return 0
