"""
Just add a function. It will be called automatically every 10s.
"""

lastCo2Value = 800

def co2_checker(room_ctl):
    global lastCo2Value

    if room_ctl.twin.get_co2() > 1000 and lastCo2Value < 1000:
        room_ctl.ble_interface.notifications.put("Please Open the Window C02 level is belastend")
        lastCo2Value = room_ctl.twin.get_co2()


    if room_ctl.twin.get_co2() < 800 and lastCo2Value > 1000:
        room_ctl.ble_interface.notifications.put("You can close the window now.")
        lastCo2Value = room_ctl.twin.get_co2()


def energy_publisher(room_ctl):
    for dev in room_ctl.devices:
        if dev.name == "building_mqtt_exporter":
            dev.propose_and_commit(room_ctl.twin.get_total_current_consumption())