from vector import Vector
from quaternion import Quaternion


class Odometry:
    def __init__(self):
        self.position = Vector()
        self.orientation = Quaternion()
