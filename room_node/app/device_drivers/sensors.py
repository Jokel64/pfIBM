import time

from .prototypes import Sensor
import paho.mqtt.client as mqtt
import logging as lg
from room_node.app.gateway_drivers.mqtt import MQTTGateway


class RoomClimate(Sensor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_state(self):
        state = self.gateway.delegate_from_physical_device()
        return state


class Lighting(Sensor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_state(self):
        state = self.gateway.delegate_from_physical_device()
        return state


class WeatherInfo(Sensor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.topic = ""
        if "topic" in kwargs:
            self.topic = kwargs["topic"]
        else:
            lg.error(f"{self.name} does not have a specified weather topic!")

        if isinstance(self.gateway, MQTTGateway):
            counter = 0
            while not self.gateway.ready:
                time.sleep(0.1)
                counter += 1
                if counter > 50:
                    lg.error(f"{self.name} couldn't connect to its gateway! This sensor will not work properly!")
                    break
            self.gateway.subscribe(self.topic, self.name)

    def get_state(self):
        return self.gateway.delegate_from_physical_device(**{"topic": self.topic})


class CO2(Sensor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.topic = ""
        if "topic" in kwargs:
            self.topic = kwargs["topic"]
        else:
            lg.error(f"{self.name} does not have a specified weather topic!")

        if isinstance(self.gateway, MQTTGateway):
            counter = 0
            while not self.gateway.ready:
                time.sleep(0.1)
                counter += 1
                if counter > 50:
                    lg.error(f"{self.name} couldn't connect to its gateway! This sensor will not work properly!")
                    break
            self.gateway.subscribe(self.topic, self.name)

    def get_state(self):
        return self.gateway.delegate_from_physical_device(**{"topic": self.topic})
