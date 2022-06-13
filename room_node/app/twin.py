from device_drivers.prototypes import Actuator, Sensor, Device
from device_drivers.actuators import *
from device_drivers.sensors import *


class Twin:
    def __init__(self, devices: list[Device]):
        self.devices = devices
        self.weather_info = self._get_weather_info_device()

    def _get_weather_info_device(self):
        for dev in self.devices:
            if isinstance(dev, WeatherInfo):
                return dev
        lg.warning("No WeatherInfo Device was found. The lighting will not be able to operate efficiently!")
        return None

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
                    lux += dev.proposed_state * (1-self.weather_info.get_state()["cloudy"]) * self.weather_info.get_state()["sun_lux"] * 0.01
        return lux
