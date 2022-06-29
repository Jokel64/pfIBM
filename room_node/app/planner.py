from device_drivers.prototypes import Actuator, Sensor, Device
from device_drivers.actuators import *
from device_drivers.sensors import *
from twin import Twin
import random


class Planner:

    def __init__(self, devices, twin: Twin):
        self.devices = devices
        self.twin = twin

    def plan(self, goal, goal_type, n_iterations=100000):

        print("start planning")

        #init goal state (for keeping non goal values near the previous value)
        if goal_type == "temperature":
            goal_state = {"brightness": self.twin.get_brightness(), "temperature": goal}
        if goal_type == "brightness":
            goal_state = {"brightness": goal, "temperature": self.twin.get_room_temp()}

        # init best config and very high best values
        best_config = {}
        best_values = {"brightness": 1000000, "temperature": 1000000}

        # episodes
        for _ in range(n_iterations):

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

                # TODO HVAC planning
                #if isinstance(dev, HVAC):

                if isinstance(dev, WindowBlinds):
                    random_dev_val = random.random()
                    usable_device = True

                if usable_device:
                    # propose random value for device for simulation
                    dev.propose(random_dev_val)
                    # save dev and random value in the current config
                    dev_config[dev] = random_dev_val

            # save values for current config
            values = {"brightness": self.twin.get_brightness(), "temperature": self.twin.get_room_temp()}
            temp_truth = []
            # loop over values to check if they are better than the previous best
            for key, val in values.items():
                if abs(goal_state[key]-val) < abs((goal_state[key] - best_values[key])):
                    temp_truth.append(True)
                else:
                    temp_truth.append(False)

            # new best only if all values are closer to the goal
            new_best_state = True
            for k in temp_truth:
                new_best_state = new_best_state*k

            # set new best values and config
            if new_best_state:
                best_values = values
                best_config = dev_config

        # loop over best config after n_timesteps
        for dev, val in best_config.items():

            #commit best config
            dev.propose_and_commit(val)

        print("finished planning")
