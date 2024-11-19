from abc import ABC, abstractmethod

# TODO: адаптировать Planner под абстрактный класс и импортировать во все планеры, наследуя при этом
#       основные классы каждого планировщика от абстрактного общего класса

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
    def setVelocity(self):
        pass