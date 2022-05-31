from enum import Enum

import logging as lg

from os.path import exists
import xml.etree.ElementTree as ET
from gateway_drivers.phillips_hue import PhillipsHueGateway
from gateway_drivers.i2c import I2cGateway
from gateway_drivers.pfIBM_sim import PfSim
from gateway_drivers.prototypes import Gateway
from device_drivers.prototypes import Device, DeviceTypes
from device_drivers.actuators import *
from device_drivers.sensors import *

ROOM_CONFIG = "config/room-config.xml"


class RoomController:
    def __init__(self):
        if exists(ROOM_CONFIG):
            self.config = ET.parse(ROOM_CONFIG).getroot()
        else:
            lg.error("No room-config.xml found in config directory! Exiting...")
            exit(1)

        self.gateways: dict[str, Gateway] = {}
        self.devices: list[Device] = []
        self.load_room_config()

    def load_room_config(self):
        gateways = self.config.find("gateways")
        devices = self.config.find("devices")
        if gateways is None or devices is None:
            lg.error("No gateways/devices are defined!")
            exit(1)
        for gw in gateways:
            id = gw.text
            if gw.tag == "phillips_hue":
                self.gateways[id] = PhillipsHueGateway(**gw.attrib)
            elif gw.tag == "i2c":
                self.gateways[id] = I2cGateway(**gw.attrib)
            elif gw.tag == "pfIBM_sim":
                self.gateways[id] = PfSim(**gw.attrib)
            else:
                lg.error(f"Gateway of type {gw.tag} is not supported!")

        for dv in devices.find("actuators"):
            gw = self.get_gateway_from_device_definition(dv)
            if dv.tag == "lamp":
                self.devices.append(Lamp(gateway_ref=gw, **dv.attrib))
            elif dv.tag == "powersocket":
                self.devices.append(PowerSocket(gateway_ref=gw, **dv.attrib))
            elif dv.tag == "hvac":
                self.devices.append(HVAC(gateway_ref=gw, **dv.attrib))
            elif dv.tag == "blinds":
                self.devices.append(Blinds(gateway_ref=gw, **dv.attrib))
            else:
                lg.error(f"The device type {dv.tag} is not supported. Ignoring...")

        for dv in devices.find("sensors"):
            gw = self.get_gateway_from_device_definition(dv)
            if dv.tag == "climate":
                self.devices.append(Climate(gateway_ref=gw, **dv.attrib))
            elif dv.tag == "lighting":
                self.devices.append(Lighting(gateway_ref=gw, **dv.attrib))
            else:
                lg.error(f"The device type {dv.tag} is not supported. Ignoring...")

        lg.info("Config loaded successfully!")

    def get_gateway_from_device_definition(self, device: ET):
        gw_name = device.attrib["gateway"]
        if not gw_name in self.gateways:
            lg.error(f"Gateway {gw_name} unknown!")
            exit(1)
        return self.gateways[gw_name]