import time
import json

if __name__ == "__main__":
    from prototypes import Gateway
else:
    from .prototypes import Gateway

import paho.mqtt.client as mqtt
import logging as lg
from threading import Thread

class MQTTGateway(Gateway):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "MQTT Gateway"
        self.host = ""
        self.port = 1883
        if "port" in kwargs:
            self.port = int(kwargs["port"])

        if "host" in kwargs:
            self.host = kwargs["host"]
        else:
            ValueError(f"{self.name} needs a host to connect to!")

        self._client = mqtt.Client(self.name)
        self.ready = False

        # key: topic, value: list of client ids
        self.subscriptions = dict()
        # key: topic, value: last_message
        self.last_messages = dict()
        self.loop_thread = None
        self.init_physical_gateway()

    def _on_connect(self, client, userdata, flags, rc):
        #lg.info(f"{self.name} connected with result code {rc}")
        self.ready = True

    def _on_message(self, client, userdata, msg):
        lg.debug(f"{self.name} message received-> " + msg.topic + " " + str(msg.payload))
        print(f"{self.name} message received-> " + msg.topic + " " + str(msg.payload))
        self.last_messages[msg.topic] = msg.payload.decode("utf-8")

    def _loop(self):
        self._client.loop_forever()

    def subscribe(self, topic: str, identifier: str, qos=0):
        if self.ready:
            if topic in self.subscriptions:
                self.subscriptions[topic].append(identifier)
            else:
                self.subscriptions[topic] = [identifier]
                self.last_messages[topic] = ""
            lg.debug(f"{identifier} subscribing to topic '{topic}'")
            self._client.subscribe(topic, qos)
        else:
            lg.error("Couldn't subscribe in MQTT gateway: Client wasn't ready yet.")

    def init_physical_gateway(self):
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(self.host, self.port)
        self.loop_thread = Thread(target=self._loop, daemon=True)
        self.loop_thread.start()

    def delegate_to_physical_device(self, value, **kwargs):
        if not self.ready:
            lg.error("MQTT-Gateway couldnt send message as it is not ready yet.")
            return
        if "topic" not in kwargs:
            lg.error("MQTT-Gateway delegate to physical needs a topic in kwargs")
            return
        print(f"Sending {value} to {kwargs['topic']}")
        self._client.publish(kwargs["topic"], value)

    def delegate_from_physical_device(self, **kwargs):
        if self.devmode or self.last_messages[kwargs["topic"]] == '':
            res = self.handle_devmode(**kwargs)
            return res
        if "topic" in kwargs:
            return json.loads(self.last_messages[kwargs["topic"]])
        else:
            lg.error(f"{self.name} delegation needs a topic!")
            return None

    def handle_devmode(self, **kwargs):
        if kwargs["topic"] == "/weather":
            return {"cloudy": 0.8, "sun_lux": 50000, "temp": 20}
        elif kwargs["topic"] == "/co2":
            return 414
        return "no dev mode value specified."


if __name__ == "__main__":
    lg.basicConfig(format='[%(levelname)s] %(filename)s: %(message)s', level=lg.DEBUG)

    mc = MQTTGateway(**{"host": "127.0.0.1"})
    while not mc.ready:
        time.sleep(1)
    mc.subscribe("/weather", "tes ter")

    time.sleep(5)
    lg.info(f"This is my message: {mc.delegate_from_physical_device(**{'topic': '/weather'})}")
