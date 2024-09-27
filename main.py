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
    
    api.takeoff(altitude=1)
    # time.sleep(1)
    # api.land()
    # api.navigate(1, 0, 3, 180, False)
    
    update_thread.join()

if __name__ == "__main__":
    main()