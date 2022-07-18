from rest_api import app, set_room_controller
import logging as lg
from room_controller import RoomController
import os
import planner

from device_drivers.actuators import *
from room_node.app.ble_interface import BLENetworkMock

if __name__ == "__main__":
    #lg.basicConfig(format='[%(levelname)s] %(filename)s: %(message)s', level=lg.DEBUG)
    rc = RoomController(devmode=True)
    set_room_controller(rc)



    def value_cb():
        ble_interface.ist_temp = rc.twin.get_room_temp()
        ble_interface.ist_ligting = rc.twin.get_brightness()

        rc.plan("brightness", ble_interface.soll_ligting)
        rc.plan("temperature", ble_interface.soll_temp)

    print("Starting BLE Interface Module Test")
    ble_interface = BLENetworkMock()
    ble_interface.registerNewValuesCB(value_cb)



    ble_interface.notifications.put("This Is a test")

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
