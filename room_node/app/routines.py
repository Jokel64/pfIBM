"""
Just add a function. It will be called automatically every 10s.
"""
def co2_checker(room_ctl):
    print("Wowzers: ", room_ctl.twin.get_co2())
