from rest_api import app, set_room_controller
import logging as lg
from room_controller import RoomController
import os
import planner

from device_drivers.actuators import *
from room_node.app.ble_interface import BLENetworkMock

if __name__ == "__main__":
    #lg.basicConfig(format='[%(levelname)s] %(filename)s: %(message)s', level=lg.DEBUG)
    rc = RoomController(devmode=False)
    set_room_controller(rc)

    # init some values (neccessary for twin calculations before planning)
    for dev in rc.devices:
        if isinstance(dev, WindowBlinds):
            dev.propose(0.2)

        if isinstance(dev, Lamp):
            dev.propose(1)

    rc.plan("brightness", 420)
    rc.plan("temperature", 20)
    rc.plan("EAS", 0.4)

    app.run(host="0.0.0.0", use_reloader=False)
