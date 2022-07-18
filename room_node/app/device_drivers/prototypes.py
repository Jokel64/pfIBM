from enum import Enum
import logging as lg


class Device:
    def __init__(self, gateway_ref, name="Undefined",  **kwargs):
        self.name = name
        self.gateway = gateway_ref
        self.last_state = None

    def __str__(self):
        return self.name


class Sensor(Device):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_state(self):
        lg.error(f"{self.name} has no valid implementation of proposed_state!")


class Actuator(Device):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.proposed_state = None
        self.max_watts = float(kwargs["watt"])
    """
    Proposes a new state that needs to be checked. 
    !Sets self.proposed_state & self.proposed_valid
    """
    def propose(self, new_val):
        lg.error(f"{self.name} has no valid implementation of proposed_state!")

    """
    Commits the proposed state to the gateway
    """
    def commit(self):
        if self.gateway.delegate_to_physical_device(self.proposed_state) == 0:
            self.last_state = self.proposed_state
            return 0
        else:
            self.last_state = None
            return 1
    """
    Does the propose and commit in one step.
    """
    def propose_and_commit(self, new_val):
        if self.propose(new_val) == 0:
            self.commit()
        else:
            lg.error("Error committing proposed value to the gateway.")

    """
    Calculates its current energy consumption
    """
    def get_current_proposed_watts(self):
        if isinstance(self.proposed_state, float) or isinstance(self.proposed_state, int):
            return self.max_watts * self.proposed_state
        else:
            lg.error(f"{self.name} doesnt have a valid defintion of get_current-proposed_watts as its proposed state "
                     f"is non-numerical")
            return 0
