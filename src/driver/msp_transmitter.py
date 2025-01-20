import time
from abc import ABC, abstractmethod
from threading import Lock, Thread
import logging
import socket
import serial


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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.buffersize = 4096  # Default buffer size for UDP
        self.closed = False
        self.timeout_exception = socket.timeout
        self.host, self.port = address
        self.timeout = None

    def connect(self, timeout=1/500):
        self.sock.settimeout(timeout)
        self.closed = False
        self.timeout = timeout

    def disconnect(self):
        if not self.sock:
            raise Exception("Cannot close, socket never created")
        self.closed = True
        self.sock.close()

    def reconnect(self):
        self.sock.settimeout(self.timeout)
        self.closed = False

    def send(self, bufView: bytearray, blocking: bool = True, timeout: int = -1):
        sent = self.sock.sendto(bufView, (self.host, self.port))
        if not sent:
            raise RuntimeError("socket connection broken (send)?")
        return sent

    def receive(self, size: int):
        recvbuffer = b''
        try:
            if size:
                recvbuffer, _ = self.sock.recvfrom(size)
            else:
                recvbuffer, _ = self.sock.recvfrom(self.buffersize)
        except socket.timeout:
            return recvbuffer
        if not recvbuffer:
            raise RuntimeError("socket connection broken (recv)?")

        return recvbuffer

    def local_read(self, size=1):
        return self.sock.recvfrom(size)[0]
        
        
class TCPTransmitter(Transmitter):
    def __init__(self, address):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.buffersize = self.sock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
        
        self.closed = False
        self.timeout_exception = socket.timeout
        self.host = "192.168.2.113"
        self.port = 5760
        self.timeout = None
        
    def connect(self, timeout=1/500):
        self.sock.connect((self.host, self.port))
        self.sock.settimeout(timeout)
        self.closed = False
        self.timeout = timeout

    def disconnect(self):           
        if not self.sock:
            raise Exception("Cannot close, socket never created")
        self.closed = True
        self.sock.close()
        
    def reconnect(self, attempts=3, delay=1):
        for attempt in range(attempts):
            try:
                self.sock.close()
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.sock.connect((self.host, self.port))
                self.sock.settimeout(self.timeout)
                self.closed = False
                return
            except (ConnectionResetError, OSError) as e:
                if attempt < attempts - 1:
                    time.sleep(delay)
                else:
                    raise e

    def send(self, bufView:bytearray, blocking:bool = True, timeout:int = -1):
        try:
            sent = self.sock.send(bufView)
            if not sent:
                raise RuntimeError("socket connection broken (send)?")
            return sent
        except (BrokenPipeError, ConnectionResetError, OSError):
            self.reconnect()
            sent = self.sock.send(bufView)
            if not sent:
                raise RuntimeError("socket connection broken (send)?")
            return sent
    
    def receive(self, size:int):
        recvbuffer = b''
        try:
            if size:
                recvbuffer = self.sock.recv(size)
            else:
                recvbuffer = self.sock.recv(self.buffersize)
        except socket.timeout:
            return recvbuffer
        if (not recvbuffer):
            raise RuntimeError("socket connection broken (recv)?")

        return recvbuffer
    
    def local_read(self, size=1):
        return self.sock.recv(size)


class SerialTransmitter(Transmitter):
    def __init__(self, port: str, baud):
        super().__init__()
        self.write_lock = Lock()
        self.read_lock = Lock()
        self.serial_client = serial.Serial()
        self.serial_client.port = port
        self.serial_client.baudrate = baud
        self.serial_client.bytesize = serial.EIGHTBITS
        self.serial_client.parity = serial.PARITY_NONE
        self.serial_client.stopbits = serial.STOPBITS_ONE
        self.serial_client.timeout = 1
        self.serial_client.xonxoff = False
        self.serial_client.rtscts = False
        self.serial_client.dsrdtr = False
        self.serial_client.writeTimeout = 1

    def connect(self):
        if self.is_connect is False:
            try:
                self.serial_client.open()
                self.is_connect = True

                logging.info("Serial connect")
            except:
                logging.error("Cant connect to serial")
        else:
            logging.info("Serial_client is connected already")


    def disconnect(self):
        if self.is_connect is True:
            try:
                self.serial_client.close()
                self.is_serial_open = False

                logging.info("Close serial")
            except:
                logging.error("Cant close serial")
        else:
            logging.info("Serial_client is disconnected already")
    
    def send(self, bufView:bytearray, blocking:bool=True, timeout:int=-1):
        res = 0
        if self.write_lock.acquire(blocking, timeout):
            try:
                res = self.serial_client.write(bufView) 
            finally:
                self.write_lock.release()
                if res > 0:
                    logging.info("RAW message sent by serial: {0}".format(bufView))  
                return res
                
    def receive(self, size:int, timeout:int = 10):

        with self.read_lock: 
            local_read = self.serial_client.read
            timeout = time.time() + timeout
            while True:
                if time.time() >= timeout:
                    logging.warning("Timeout occured when receiving a message")
                    break
                msg_header = local_read()
                if msg_header:
                    if ord(msg_header) == 36: 
                        break

            msg = local_read(size - 1) 

            logging.info("Recived msg_header: {0}; msg: {1}".format(msg_header,msg))
            return msg_header, msg
        
    def local_read(self, size:int):
        return self.serial_client.read(size)


def serialize(address, type):
    match type:
        case "udp":
            return UDPTransmitter(address)
        case "tcp":
            return TCPTransmitter(address)
        case "serial":
            return SerialTransmitter(address, 115200)
