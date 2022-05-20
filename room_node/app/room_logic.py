from rest_api import app, menu_items
from os.path import exists
import xml.etree.ElementTree as ET
import logging as lg

ROOM_CONFIG = "config/room-config.xml"


class RoomController:
    def __init__(self):
        if exists(ROOM_CONFIG):
            self.config = ET.parse(ROOM_CONFIG)
        else:
            lg.error("No room-config.xml found in config directory! Exiting...")
            exit(1)

        lg.info(self.config)


if __name__ == "__main__":
    lg.basicConfig(format='%(levelname)s:%(message)s', level=lg.DEBUG)
    rc = RoomController()

    menu_items.append(
        {
            "name": "Settings",
            "tooltip": "Settings are here",
            "icon": "bx-grid-alt"
        })
    menu_items.append(
        {
            "name": "Settings 2",
            "tooltip": "Settings are here",
            "icon": "bx-grid-alt"
        })
    app.run(host="0.0.0.0")
