import paho.mqtt.publish as publish


def publish_co2(val):
    publish.single("/co2", val)


if __name__ == "__main__":
    value = 1200
    publish_co2(value)
