from abc import ABC, abstractmethod
import logging
import socket


class Transmitter(ABC):

    @abstractmethod
    def __init__(self):
        self.is_connect = False

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send(self, bufView, blocking=True, timeout=-1):
        pass

    @abstractmethod
    def receive(self, size, timeout=10):
        pass

    @abstractmethod
    def local_read(self, size):
        pass


class UDPTransmitter(Transmitter):

    def __init__(self, address):

        super().__init__()

        self.address = address
        self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):

        if self.is_connect is False:

            try:
                self.udp_client.connect(self.address)
                self.is_connect = True

                logging.info("tcp connect")

            except:
                logging.error("cant connect to tcp")

        else:
            logging.info("tcp_client is connected already")

    def disconnect(self):

        if self.is_connect is True:

            try:
                self.udp_client.close()
                self.is_connect = False

                logging.info("close tcp")
            except:
                logging.error("cant close tcp")

        else:
            logging.info("tcp_client is disconnected already")

    def send(self, bufView: bytearray, blocking: bool = True, timeout: int = -1):

        try:
            res = self.udp_client.send(bufView)
            logging.info("RAW message sent by tcp: {0}".format(bufView))
            res = 1

        except:
            logging.error("Cant send bufView to tcp")
            res = 0

        return res

    def receive(self, size: int, timeout: int = 1):

        try:
            msg_header = self.udp_client.recv(1)
            msg = self.udp_client.recv(size - 1)

            logging.info("Recived msg_header: {0}; msg: {1}".format(msg_header, msg))

            return msg_header, msg

        except:
            logging.info("Cant recive msg")

    def local_read(self, size):
        return self.udp_client.recv(size)
