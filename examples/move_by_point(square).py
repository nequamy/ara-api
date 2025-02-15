from lib.AppliedRoboticsAviaAPI import AppliedRoboticsAviaAPI
import time

def main():
    api = AppliedRoboticsAviaAPI()
    
        
    api.takeoff(1)
    time.sleep(3)

    api.move_by_point(0.5, 0)
    time.sleep(3)
    api.move_by_point(0.5, 0.5)
    time.sleep(3)
    api.move_by_point(0, 0.5)
    time.sleep(3)
    api.move_by_point(0, 0)
    time.sleep(3)
    
    
    
    api.land()

if __name__ == "__main__":
    main()