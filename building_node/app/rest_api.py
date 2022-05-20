import flask
from flask import jsonify
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True

menu_items = [
    {
        "name": "Dashboard",
        "tooltip": "This is the dashboard",
        "icon": "bx-grid-alt"
    }
]

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def home():
    return jsonify(menu_items)


@app.route('/Dashboard', methods=['GET'])
def Dashboard():
    dummy = [{
        "name": "This is some data",
        "value": 234,
        "type": "number"
    },
        {
            "name": "This is even more data",
            "value": 678
        }]
    return jsonify(dummy)


@app.route('/Settings', methods=['GET'])
def Settings():
    dummy = [{
        "name": "asdfasdfasdf",
        "value": 2341234
    },
        {
            "name": "sdfgsdfgdsfg",
            "value": 67823452345
        }]
    return jsonify(dummy)


if __name__ =="__main__":
    app.run()
