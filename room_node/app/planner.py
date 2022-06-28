from device_drivers.prototypes import Actuator, Sensor, Device
from device_drivers.actuators import *
from device_drivers.sensors import *
from twin import Twin
import random


class Planner:

    def __init__(self, devices, twin: Twin):
        self.devices = devices
        self.twin = twin

    def plan(self, goal, goal_type, n_iterations=10000):

        # init best values
        best_config = {}
        best_value = 1000000

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

            # check for type of the goal and get value from simulation according to the random values
            if goal_type == "temperature":
                value = self.twin.get_room_temp()
            if goal_type == "brightness":
                value = self.twin.get_brightness()

            # check if the current episode confg is better that the previous best
            print(goal)
            print(value)
            print(best_value)
            print(goal - value)
            print(goal - best_value)
            if abs(goal - value) < abs(goal - best_value):
                print("better")
                # save new best values
                best_value = value
                best_config = dev_config
            else:
                print("worse")

        # loop over best config after n_timesteps
        for dev, val in best_config.items():

            #commit best config
            dev.propose_and_commit(val)
