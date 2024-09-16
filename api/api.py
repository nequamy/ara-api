from lib.api_driver import MultirotorControl
from lib.transmitter import UDPTransmitter

from data.altitude import Altitude
from data.attitude import Attitude
from data.barometer import Barometer
from data.battery import Bsattery
from data.channels import Channels
from data.flags import Flags
from data.odom import Odometry


class api(object):
    def __init__(self):
        self.connector = UDPTransmitter(('192.168.2.1', 14550))
        self.driver = MultirotorControl(self.connector)

        self.altitude = Altitude()
        self.attitude = Attitude()
        self.barometer = Barometer()
        self.battery = Battery()
        self.channels = Channels()
        self.flags = Flags()
        self.odom = Odometry()
        
        self.is_armed = False
        self.airmode = False
        

    def update_loop(self) -> None:
        self.update_data()

        self.load_data()

    def update_data(self) -> None:
        pass # TODO: fill the load_data to FC Function

    def load_data(self) -> None:
        pass # TODO: fill the load_data to FC Function

    def takeoff(self, altitude: int = None) -> bool:
        return self.exec(cmd="takeoff", z=altitude)

    def navigate(self, x: float = None, y: float = None, z: float = None) -> bool:
        return self.exec(cmd="navigate", x=x, y=y)

