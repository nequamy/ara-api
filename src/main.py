from app import Api
from lib.drone import ARA_mini
from lib.stream import Stream

from threading import Thread
import time

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


def main():
    drone = ARA_mini()
    api = Api("192.168.2.113", 5760, drone)
    stream = Stream()

    stream_thread = Thread(target=stream.stream, args=(), daemon=True)
    update_thread = Thread(target=api.update_loop, args=(), daemon=True)
    stream_thread.start()
    update_thread.start()

    time.sleep(1)

    ######## Начало кода ########

    api.set_arm_state(1)
    api.set_nav_state(2)

    print(api.go_to_xy(1, 0, 0))

    ######## Конец кода ########

    update_thread.join()
    stream_thread.join()


if __name__ == "__main__":
    main()
