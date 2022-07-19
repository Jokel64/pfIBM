from device_drivers.prototypes import Actuator, Sensor, Device
from device_drivers.actuators import *
from device_drivers.sensors import *
from twin import Twin
import random


class Planner:

    def __init__(self, devices, twin: Twin):
        self.devices = devices
        self.twin = twin

    def execute_routine(self):
        pass

    def plan(self, goal, goal_type, EAS, n_iterations=1e5):

        print(f"start planning for {goal_type} to {goal}")

        #init goal state (for keeping non goal values near the previous value)
        if goal_type == "brightness":
            goal_state = {"brightness": goal, "temperature": self.twin.get_room_temp(), "EAS": EAS}
        if goal_type == "temperature":
            goal_state = {"brightness": self.twin.get_brightness(), "temperature": goal, "EAS": EAS}
        if goal_type == "EAS":
            goal_state = {"brightness": self.twin.get_brightness(), "temperature": self.twin.get_room_temp(), "EAS": EAS}

        # init best config and very high best values
        best_config = {}
        best_values = {"brightness": 1e6, "temperature": 1e6, "EAS": 1e6}

        # episodes
        for _ in range(int(n_iterations)):

            # init current config
            dev_config = {}

            # loop over devices; apply random value according to device
            for dev in self.devices:

                usable_device = False

                if isinstance(dev, Lamp):
                    if dev.dimmable:
                        random_dev_val = random.random()
                        usable_device = True
                    else:
                        random_dev_val = random.randint(0,1)
                        usable_device = True

                if isinstance(dev, WindowBlinds):
                    random_dev_val = random.random()
                    usable_device = True

                if isinstance(dev, HVAC):
                    random_temp = random.randrange(10, 40)
                    random_strength = random.random()
                    random_dev_val = [random_temp, random_strength]
                    usable_device = True

                if isinstance(dev, WindowBlinds):
                    random_dev_val = random.random()
                    usable_device = True

                if usable_device:
                    # propose random value for device for simulation
                    dev.propose(random_dev_val)
                    # save dev and random value in the current config
                    dev_config[dev] = random_dev_val

            # save values for current config
            values = {"brightness": self.twin.get_brightness(), "temperature": self.twin.get_room_temp(), "EAS": self.twin.get_EAS()}
            temp_truth = []
            # loop over values to check if they are better than the previous best
            for key, val in values.items():
                if key == "EAS":
                    continue
                if abs(goal_state[key]-val) < abs((goal_state[key] - best_values[key])):
                    temp_truth.append(True)
                else:
                    temp_truth.append(False)

            # new best only if all values are closer to the goal
            new_best_state = True
            for k in temp_truth:
                new_best_state = new_best_state*k

            #check if Environmental Awareness Score is satisfied
            if new_best_state:
                if values.get("EAS") < goal_state.get("EAS"):
                    new_best_state = False

            # set new best values and config
            if new_best_state:
                best_values = values
                best_config = dev_config

        # loop over best config after n_timesteps
        for dev, val in best_config.items():

            #commit best config
            dev.propose_and_commit(val)

        print(f"start planning for {goal_type}")
