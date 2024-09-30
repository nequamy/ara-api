from app import Api
from lib.drone import ARA_mini

from threading import Thread
import time


def main():
    drone = ARA_mini()
    api = Api("192.168.2.1", 5760, drone)

    update_thread = Thread(target=api.update_loop, args=(), daemon=True)
    update_thread.start()

    time.sleep(1)

    api.set_arm_state(True)
    api.set_nav_state(2)

    # print("takeoff")
    # api.takeoff(altitude=1)
    # time.sleep(1)
    # print("landing")
    # api.land()
    api.navigate(1, 0, 1, 90, False)
    api.navigate(1, 1, 1, 180, False)
    api.navigate(0, 1, 1, 270, False)
    api.navigate(0, 0, 1, 0, False)

    # api.navigate(1, 0, 1, 0, False)
    # api.navigate(1, 1, 1, 0, False)
    # api.navigate(0, 1, 1, 0, False)
    # api.navigate(0, 0, 1, 0, False)
    #
    # api.navigate(1, 0, 1, 0, False)
    # api.navigate(1, 1, 1, 0, False)
    # api.navigate(0, 1, 1, 0, False)
    # api.navigate(0, 0, 1, 0, False)
    #
    # api.navigate(1, 0, 1, 0, False)
    # api.navigate(1, 1, 1, 0, False)
    # api.navigate(0, 1, 1, 0, False)
    # api.navigate(0, 0, 1, 0, False)
    #
    # api.navigate(1, 0, 1, 0, False)
    # api.navigate(1, 1, 1, 0, False)
    # api.navigate(0, 1, 1, 0, False)
    # api.navigate(0, 0, 1, 0, False)
    #
    # api.navigate(1, 0, 1, 0, False)
    # api.navigate(1, 1, 1, 0, False)
    # api.navigate(0, 1, 1, 0, False)
    # api.navigate(0, 0, 1, 0, False)

    update_thread.join()


if __name__ == "__main__":
    main()
