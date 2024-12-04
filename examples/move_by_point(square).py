from lib.AppliedRoboticsAviaAPI import AppliedRoboticsAviaAPI
import time

# TODO: написать рабочий пример

def main():
    api = AppliedRoboticsAviaAPI()

    api.takeoff(1.5)
    time.sleep(3)

    api.move_by_point(1, 0, 1)
    time.sleep(3)
    api.move_by_point(1, 1, 1)
    time.sleep(3)
    api.move_by_point(0, 1, 1)
    time.sleep(3)
    api.move_by_point(0, 0, 1)
    time.sleep(3)

    api.land()

if __name__ == "__main__":
    main()