from data.quaternion import Quaternion
from data.vector import Vector

class Attitude:
    def __init__(self):
        self.orientation = Quaternion()
        self.body_rate = Vector()
