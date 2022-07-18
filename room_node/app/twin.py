from device_drivers.prototypes import Actuator, Sensor, Device
from device_drivers.actuators import *
from device_drivers.sensors import *


class Twin:
    #def __init__(self, devices: list[Device]):
    def __init__(self, devices):
        self.devices = devices
        self.weather_info = self._get_weather_info_device()

        self.total_max_watts = 0
        for dev in devices:
            if isinstance(dev, Actuator):
                self.total_max_watts += dev.max_watts

    def _get_weather_info_device(self):
        for dev in self.devices:
            if isinstance(dev, WeatherInfo):
                return dev
        lg.warning("No WeatherInfo Device was found. The lighting will not be able to operate efficiently!")
        return None

    def get_EAS(self):
        curr = 0
        for dev in self.devices:
            if isinstance(dev, Actuator):
                curr += dev.get_current_proposed_watts()

        return curr / self.total_max_watts

    def get_brightness(self):
        lux = 0

        for dev in self.devices:
            if isinstance(dev, Actuator) and dev.proposed_state is None:
                lg.debug(f"Skipping {dev} in brightness calculation since its proposed state is None.")
                continue
            if isinstance(dev, Lamp):
                lux += dev.max_mean_lux * dev.proposed_state
            if isinstance(dev, WindowBlinds):
                if self.weather_info is not None:
                    # Assuming that only 1% of the lux actually comes into the room
                    try:
                        cloudy = self.weather_info.get_state()["cloudy"]
                        sunlux = self.weather_info.get_state()["sun_lux"]
                        lux += dev.proposed_state * (1-cloudy) * sunlux * 0.01
                    except Exception as e:
                        lg.error(f"Couldn't calculate brightness due to error in environment calculation: {e}")
        return lux

    def get_room_temp(self) -> float:
        temp = 5
        if self.weather_info is not None:
            temp = self.weather_info.get_state()["temp"]

        for dev in self.devices:
            if isinstance(dev, WindowBlinds):
                if self.weather_info is not None:
                    temp += (1-self.weather_info.get_state()["cloudy"])*10*dev.proposed_state
            if isinstance(dev, Lamp):
                temp += 0.1
            if isinstance(dev, HVAC) and isinstance(dev.proposed_state, list) and len(dev.proposed_state) == 2:
                if dev.proposed_state[1] == 1:
                    return dev.proposed_state[0]
                else:
                    temp += (dev.proposed_state[0] - temp) * dev.proposed_state[1]
        return temp


