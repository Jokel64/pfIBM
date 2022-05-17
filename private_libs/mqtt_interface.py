import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time
import paho.mqtt.publish as publish


class MQTT_Subscriber_Simple:

    def __init__(self, topic_name, broker_address="127.0.0.1"):
        self.broker_address = broker_address
        self.topic_name = topic_name

    def get_message(self):
        msg = subscribe.simple(self.topic_name, hostname=self.broker_address)
        return msg


class MQTT_Publisher_Simple:

    def __init__(self, topic_name, broker_address="127.0.0.1"):
        self.broker_address = broker_address
        self.topic_name = topic_name

    def send_message(self, message="simple message"):
        publish.single(self.topic_name, message, hostname=self.broker_address)

class MQTT_Subscriber:

    result = 0
    state = True

    def __init__(self, instance_name, topic_name, broker_address="127.0.0.1"):
        self.broker_address = broker_address
        self.instance_name = instance_name
        self.topic_name = topic_name
        self.client = mqtt.Client(self.instance_name)
        self.client.connect(self.broker_address)
        self.client.on_message=self.on_message

        #self.loop(logging=False)

    def get_message(self, callback_function):
        subscribe.callback(callback_function, self.topic_name, hostname=self.broker_address)

    def get_message_simple(self):
        msg = subscribe.simple(self.topic_name, hostname=self.broker_address)
        return msg

    def on_log(self, client, userdata, level, buf):
        print("log: ", buf)

    def on_message(self, client, userdata, message):
        #print("message received " ,str(message.payload.decode("utf-8")))
        #print("message topic=",message.topic)
        #print("message qos=",message.qos)
        #print("message retain flag=",message.retain)
        self.result = str(message.payload.decode("utf-8"))
        print(self.result)

    def loop(self, logging=True):
        while True:
            self.client.loop_start()
            if logging:
                self.client.on_log = self.on_log
            self.client.subscribe(self.topic_name)
            self.client.loop_stop()
            #time.sleep(1)

    def single(self, logging=True):
        self.client.loop_start()
        if logging:
            self.client.on_log = self.on_log
        self.client.subscribe(self.topic_name)
        self.client.loop_stop()

class MQTT_Publisher:

    def __init__(self, instance_name, topic_name, broker_address="127.0.0.1"):
        self.broker_address = broker_address
        self.instance_name = instance_name
        self.topic_name = topic_name
        self.client = mqtt.Client(self.instance_name)
        self.client.connect(self.broker_address)

    def on_log(self, client, userdata, level, buf):
        print("log: ", buf)

    def loop(self, message="loop message", logging=True):
        while True:
            self.client.loop_start()
            if logging:
                self.client.on_log = self.on_log
            self.client.publish(self.topic_name, message)
            self.client.loop_stop()
            time.sleep(1)

    def single(self, message="single message", logging=True):
        #self.client.loop_start()
        #if logging:
        #    self.client.on_log = self.on_log
        #self.client.publish(self.topic_name, message)
        #self.client.loop_stop()
        publish.single("test", "single message", hostname="127.0.0.1")
