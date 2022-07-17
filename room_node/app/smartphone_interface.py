from enum import Enum
from uuid import UUID
from typing import List
from datetime import datetime
from device_drivers.prototypes import Device
from time import sleep

import json
import socket


class OccupantMotionStatus(Enum):
    UNKNOWN = 0
    SITTING = 1
    MOVING = 2


class EnvironmentalAwareness(Enum):
    I_HATE_THE_ENVIRONMENT = 0
    I_LOVE_THE_ENVIRONMENT = 1


class CalendarEntry:
    def __init__(self):
        # The time when the event is scheduled to start
        self.event_start: datetime = None

        # The time when the event is scheduled to end
        self.event_stop: datetime = None

        # The friendly name of the meeting room. If no room is used this field is left empty
        self.booked_meeting_room: str = None

        # If the beamer is planned to use in this meeting the beamer and the screen are prepared and turned on
        self.is_beamer_used: bool = False


class Calendar:
    def __init__(self):
        # This field is set to true if calendar data is provided py the users phone
        self.calendar_provided: bool = False

        # The time to which datetime the events are fetched from the device
        self.calendar_valid: datetime = datetime.now()

        # This field contains all the calendar entries of the occupant
        self.calendar_entries: List[CalendarEntry] = list()

        # In this field the estimated time when the occupant stops working is stored
        self.work_end: datetime = datetime()

        # In this field the next work start time is stored (eg. earliest meeting or defined as a seperate event)
        self.next_work_start: datetime = datetime()


class LightingCondition(Enum):
    UNKNOWN = 0  # We don't know the preference of the user
    BIO_CYCLE = 1  # Occupant wants light adapted to current weather time etc.. (AI-Planning)
    SELF_CONTROLLED = 2  # Occupant wants to control the light


class HVACCondition:
    def __init__(self):
        self.target_temperature: int = 21  # The Target Temperature the user wants for the office room
        self.allow_cooling: bool = True  # Maybe the user does not want cooling
        self.allow_heating: bool = True  # Maybe the user does not want heating


class ShadingConditions(Enum):
    UNKNOWN = 0  # We don't know the preference
    AS_DARK_AS_POSSIBLE = 1  # Occupant want's as less sun as possible in the office
    AS_LIGHT_AS_POSSIBLE = 2  # Occupant want's as much sun as possible in the office
    SELF_CONTROLLED = 2  # Occupant want's to control the shades


class OccupantInformation:
    def __init__(self):
        # This is the session id of the user which stays only the same while the occupant is in the room
        # it changes if the user leaves and re-enters the room
        self.session_id: UUID = None

        # This item stores the preferred lightning scenario of the occupant
        self.preferred_lighting_condition: LightingCondition = LightingCondition.UNKNOWN

        # This item stores the preferred shading conditions of the occupant
        self.preferred_shading_condition: ShadingConditions = ShadingConditions.UNKNOWN

        # This item stores the preferred hvac settings of the occupant
        self.preferred_hvac_condition: HVACCondition = HVACCondition()

        # This item is used to store the occupants current motion state
        self.occupant_motion_status: OccupantMotionStatus = OccupantMotionStatus.UNKNOWN

        # This item the calendar data of the user is shared
        self.calendar: Calendar = Calendar()

        # This item stores the occupant's mindset about the environment
        self.environmental_awareness: EnvironmentalAwareness = EnvironmentalAwareness.I_HATE_THE_ENVIRONMENT


class SmartphoneInterface:
    def __init__(self, device_list: List[Device]):
        self.occupants: List[OccupantInformation] = list()
        self.device_list: List[Device] = device_list

    def send_push_notification(self, notification: str):
        pass

    '''
    This is called at startup to initally transfer all devices to the UE
    '''

    def send_device_list_to_ue(self):
        device_list_dumped: str = json.dumps(self.device_list)
        print(device_list_dumped)

    '''
    This should be called if the state of the device changes so we can send the updated state to the UE 
    '''

    def update_device(self, device_to_update: Device):
        pass

    def get_current_occupants_information(self):
        return self.occupants


if __name__ == "__main__":

    msg = b'hello world'
    while True:


        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("0.0.0.0",0))
        sock.sendto(msg, ("224.0.0.0", 5005))
        sock.close()

        sleep(2)
