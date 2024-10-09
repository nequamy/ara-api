from data.vector import Vector
from data.quaternion import Quaternion


class Odometry:
    def __init__(self):
        self.position = Vector()
        self.orientation = Quaternion()
