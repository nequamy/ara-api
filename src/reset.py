from src.app import Api
from lib.drone import ARA_mini

from threading import Thread
import time

def main():
    drone = ARA_mini()
    api = Api("192.168.2.113", 5760, drone)

    update_thread = Thread(target=api.update_loop, args=(), daemon=True)
    update_thread.start()

    time.sleep(1)

    api.reset_state()

    update_thread.join()


if __name__ == "__main__":
    main()
