from rest_api import app, set_room_controller
import logging as lg
from room_controller import RoomController
import os


if __name__ == "__main__":
    lg.basicConfig(format='[%(levelname)s] %(filename)s: %(message)s', level=lg.DEBUG)

    rc = RoomController()
    rc.devices[0].set_state(0.5)

    set_room_controller(rc)

    app.run(host="0.0.0.0")
