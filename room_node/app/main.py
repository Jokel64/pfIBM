from rest_api import app, set_room_controller
import logging as lg
from room_controller import RoomController
import os

from device_drivers.actuators import *

if __name__ == "__main__":
    lg.basicConfig(format='[%(levelname)s] %(filename)s: %(message)s', level=lg.DEBUG)
    rc = RoomController(devmode=True)
    set_room_controller(rc)
    for dev in rc.devices:
        if isinstance(dev, WindowBlinds):
            dev.propose(0.2)

        if isinstance(dev, Lamp):
            dev.propose(1)

    app.run(host="0.0.0.0", use_reloader=False)
