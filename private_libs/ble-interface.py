import socket
import threading
from abc import ABC, abstractmethod


class BLEGattServer(ABC):

    @abstractmethod
    def start_advertising(self):
        pass

    @abstractmethod
    def update_state_dictionary(self):
        pass

    @abstractmethod
    def register_value_changed_cb(self):
        pass


"""
This class is used to mock BLE functionality over UDP in order to allow debugging on windows hosts
with no ble module installed
"""


class BLENetworkMock(BLEGattServer):

    def __init__(self):
        self.udp_broadcast_sock: socket = None
        self.create_socket()
        self.receiver_thread = threading.Thread(target=self.broadcast_receiver_thread)
        self.receiver_thread.start()

        self.stop_listening: bool = False

    def start_advertising(self):
        pass

    def update_state_dictionary(self):
        pass

    def register_value_changed_cb(self):
        pass

    def broadcast_receiver_thread(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("0.0.0.0", 5005))
        sock.settimeout(3)
        while not self.stop_listening:
            # sock.sendto(bytes("hello", "utf-8"), ip_co)
            data, addr = sock.recvfrom(1024)
            print(data)

    def stop_receiver_thread(self):
        self.stop_listening = True
        self.receiver_thread.join()

    def create_socket(self):
        self.udp_broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.udp_broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


if __name__ == '__main__':
    print("Starting BLE Interface Module Test")
    ble_interface = BLENetworkMock()
    ble_interface.udp_broadcast_sock.sendto(bytes("test", "utf-8"), ("255.255.255.255", 5005))
    ble_interface.stop_receiver_thread()
