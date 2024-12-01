import multiprocessing

from mdit_py_plugins.myst_blocks.index import target

from gui.app_gui import GUI
from driver.msp_service import MSPDriverManagerGRPC
from navigation.nav_service import NavigationManagerGRPC
from web.docs_app import SphinxFlaskApp

"""
Список методов API:

api.set_arm_state(state) - принимает на вход True или False для ARM и DISARM соответственно.
api.set_nav_state(state) - принимает на вход 0, 1 и 2 для ANGLE, ALTHOLD и POSHOLD соответственно.
api.takeoff(altitude) - метод для подъема дрона на высоту, отправленную в аргументах функции.
api.land(auto_disarm) - метод для опускания дрона. На вход ожидает True или False для автоматического
                        отключения двигателей.
api.go_to_xy(x, y, auto_land) - метод отправки дрона в точку (Х, Y). В случае если задан auto_land
                                дрон после перемещения в эту точку снизит высоту и выключит движки.
api.set_velocity_x(x_vel) - метод для задания скорости перемещения в оси Х.
api.set_velocity_y(y_vel) - метод для задания скорости перемещения в оси Y.
api.set_throttle(throttle) - метод для задания уровня газа/высоты коптера. Значение 2000 - 2.5м, 1000 - 0м.

Список методов Stream:
stream.get_id() - возвращает id всех распознанных маркеров.

Поля для вывода:
api.odom - словарь со значениями одометрии(['position'], ['velocity'], ['yaw'].
api.attitude - структура из папки data с ориентацией дрона в углах эйлера и в кватернионе.
api.imu - структура из папки data со значениями IMU-датчика.
api.rc_out - структура из папки data со значениями RC-каналлов, подаваемых на полетный контроллер.

P.s. строчки над "Начало кода" и под "Конец кода" оставляем не тронутыми.
"""

#
# def main():
#     gui = GUI()
#     gui.run()
#
#
# if __name__ == "__main__":
#     main()

import multiprocessing
import os
from gui.app_gui import GUI
from navigation.nav_service import NavigationManagerGRPC
from web.docs_app import SphinxFlaskApp
from driver.msp_service import main as msp_main

sphinx_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs/html/'))

class APPManager:
    def __init__(self):
        self.gui = GUI()
        self.services = []

    def add_service(self, service):
        self.services.append(service)

    def start_services(self):
        processes = []
        for service in self.services:
            process = multiprocessing.Process(target=service.main, args=())
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

if __name__ == '__main__':
    # navigationServiceManager = NavigationManagerGRPC()
    sphinxFlaskApp = SphinxFlaskApp('ARA API DOCS', sphinx_directory)

    app = APPManager()
    # app.add_service(navigationServiceManager)
    # app.add_service(sphinxFlaskApp)

    # Add MSP service using the imported main function
    msp_process = multiprocessing.Process(target=msp_main)
    sphinx_process = multiprocessing.Process(target=sphinxFlaskApp.run())
    sphinx_process.start()
    msp_process.start()

    # app.start_services()
    msp_process.join()
    sphinx_process.join()