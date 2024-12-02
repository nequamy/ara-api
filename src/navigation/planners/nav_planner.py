# TODO: адаптировать Planner под абстрактный класс и импортировать во все планеры, наследуя при этом
#       основные классы каждого планировщика от абстрактного общего класса

from abc import ABC, abstractmethod

class NavPlanner(ABC):
    @abstractmethod
    def takeoff(self):
        pass

    @abstractmethod
    def land(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def set_velocity(self, vx: float, vy: float, vz: float):
        pass

    @abstractmethod
    def check_desired_altitude(self) -> bool:
        pass

    @abstractmethod
    def check_desired_position(self) -> bool:
        pass