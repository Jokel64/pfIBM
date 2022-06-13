import flask
from flask import jsonify
from flask_cors import CORS
import logging as lg
from room_controller import RoomController

app = flask.Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

app.config["DEBUG"] = True

menu_items = [
    {
        "name": "Dashboard",
        "tooltip": "This is the dashboard",
        "icon": "bx-grid-alt"
    },
    {
        "name": "Gateways",
        "tooltip": "Gateways",
        "icon": "bx-grid-alt"
    },
    {
        "name": "Devices",
        "tooltip": "Devices",
        "icon": "bx-grid-alt"
    },
]

ctl: RoomController = None


def set_room_controller(room_controller: RoomController):
    global ctl
    ctl = room_controller


def append_dict_item(l: list, name: str, value):
    l.append({"name": name, "value": value})


@app.route('/', methods=['GET'])
def home():
    return jsonify(menu_items)


@app.route('/Dashboard', methods=['GET'])
def dashboard():
    if ctl is None:
        lg.error("Room Controller not defined!")
        return 'Internal Server Error!', 500
    ret = [{
        "name": "Current mean room-brightness",
        "value": str(ctl.twin.get_brightness()) + " lux"
    }]
    
    return jsonify(ret)


@app.route('/Gateways', methods=['GET'])
def gws():
    if ctl is None:
        lg.error("Room Controller not defined!")
        return 'Internal Server Error!', 500
    ret = []
    for gw_id in ctl.gateways:
        gw = ctl.gateways[gw_id]
        # Adding an empty value as a header
        append_dict_item(ret, f"{type(gw).__name__} [{gw_id}]", "")
        append_dict_item(ret, f"online status", gw.status.value)
    return jsonify(ret)


@app.route('/Devices', methods=['GET'])
def devices():
    if ctl is None:
        lg.error("Room Controller not defined!")
        return 'Internal Server Error!', 500
    ret = []

    for dev in ctl.devices:
        ret.append({"name": f"{dev.name} ", "value": ""})
        ret.append({"name": "Current State", "value": f"{dev.last_state}"})
        ret.append({"name": "Type", "value": f"{type(dev)}"})
        ret.append({"name": "Gateway", "value": f"{dev.gateway.name}"})


    
    return jsonify(ret)