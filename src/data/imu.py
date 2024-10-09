from data.vector import Vector
from data.quaternion import Quaternion


class Imu:
    def __init__(self):
        self.angular_velocity = Vector()
        self.linear_acceleration = Vector()
        self.orientation = Quaternion()
