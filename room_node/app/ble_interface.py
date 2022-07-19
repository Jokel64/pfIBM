import selectors
import socket
import threading
import types
from _thread import start_new_thread
from abc import ABC, abstractmethod
import time
from queue import Queue


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
        self.soc: socket = None
        self.create_socket()
        self.receiver_thread = threading.Thread(target=self.broadcast_receiver_thread)
        self.receiver_thread.start()

        self.sel = selectors.DefaultSelector()

        self.stop_listening: bool = False

        self.notifications = Queue()

        self.ist_ligting: int = 50
        self.soll_ligting: int = 300

        self.ist_temp: int = 0
        self.soll_temp: int = 20

        self.valuesChangedCB = None
        self.valuesUpdatedCB = None

    def start_advertising(self):
        pass

    def update_state_dictionary(self):
        pass

    def register_value_changed_cb(self):
        pass

    def setCurrentRoomState(self, temperature_is, lighting_is):
        self.ist_ligting = lighting_is
        self.ist_temp = temperature_is

    def registerNewValuesCB(self, callback):
        self.valuesChangedCB = callback

    def registerUpdateValuesCB(self, callback):
        self.valuesUpdatedCB  = callback

    def broadcast_receiver_thread(self):
        ServerSocket = socket.socket()
        try:
            ServerSocket.bind(("0.0.0.0", 5005))
        except socket.error as e:
            print(str(e))
        print(f'Server is listing on the port {5005}...')
        ServerSocket.listen()

        while True:
            self.accept_connections(ServerSocket)

    def client_handler(self, connection):
        connection.sendall(str.encode('You are now connected to the replay server... Type BYE to stop\n'))
        time.sleep(1)
        while True:
            data = connection.recv(2048)
            assert isinstance(data.decode, object)
            message = data.decode('utf-8')

            vals = message.split("\n")
            vals = vals[0].split(";")

            val_light = vals[0][2:]
            val_temp = vals[1]

            self.valuesUpdatedCB()

            if float(val_light) != self.soll_ligting or float(val_temp) != self.soll_temp:
                self.soll_temp = float(val_temp)
                self.soll_ligting = float(val_light)
                self.valuesChangedCB()
                print(message)


            # Here we need to calulcate the replay
            try:
                a = self.notifications.get(False)
                if a:
                    reply = f'ACTION: {a} \n'
                    connection.sendall(str.encode(reply))
            except:
                data = None

            connection.sendall(str.encode(f"{self.ist_ligting};{self.ist_temp};status\n"))
            # connection.close()

    def accept_connections(self, ServerSocket):
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(self.client_handler, (Client,))

    def stop_receiver_thread(self):
        self.stop_listening = True
        self.receiver_thread.join()

    def create_socket(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


if __name__ == '__main__':
    print("Starting BLE Interface Module Test")
    ble_interface = BLENetworkMock()

    ble_interface.notifications.put("This Is a test")

    while True:
        pass
