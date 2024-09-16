from quaternion import Quaternion
from vector import Vector

class Attitude:
    def __init__(self):
        self.quaternion = Quaternion()
        self.bodyRate = Vector()
