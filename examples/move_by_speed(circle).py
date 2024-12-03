from lib.AppliedRoboticsAviaAPI import AppliedRoboticsAviaAPI
import time
import math

def main():
    api = AppliedRoboticsAviaAPI()

    api.takeoff(1.5)
    time.sleep(3)

    radius = 1
    altitude = 1
    speed = 0.5
    points = 36  # Number of points to create a smooth circle

    for i in range(points):
        angle = 2 * math.pi * i / points
        vx = -speed * math.sin(angle)
        vy = speed * math.cos(angle)
        api.move_by_speed(vx, vy, altitude)
        time.sleep(1 / points)

    api.land()

if __name__ == "__main__":
    main()