from lib.api_driver import MultirotorControl
from lib.transmitter import UDPTransmitter

from data.altitude import Altitude
from data.attitude import Attitude
from data.barometer import Barometer
from data.battery import Battery
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

    def update_loop(self) -> None:
        self.update_data()

        self.load_data()

    def update_data(self) -> None:
        pass

    def load_data(self) -> None:
        pass

    def takeoff(self, altitude: int = None) -> bool:
        return self.exec(cmd="takeoff", z=altitude)

    def navigate(self, x: int = None, y: int = None) -> bool:
        return self.exec(cmd="navigate", x=x, y=y)

    def exec(self, cmd: str, x=None, y=None, z=None, yaw=None) -> bool:
        try:
            pass
        except Exception as e:
            print(e)
            return False
