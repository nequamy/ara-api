import time

from navigation.planners.nav_planner import NavPlanner
from navigation.utils.pid import PID
from navigation.utils.nav_drone_config import Drone
from navigation.utils.helpers import exponential_ramp, remap, constrain, transform_multirotor_speed, DataFetcher

class NavigationMultirotorPlanner(NavPlanner):
    def __init__(self, drone: Drone):
        self.roll_pid = PID(kp=2.5, kd=1.5, name="Roll")
        self.pitch_pid = PID(kp=2.5, kd=1.5, name="Pitch")
        self.yaw_pid = PID(kp=2.5, kd=1.5, name="Yaw")

        self.drone = drone
        self.grpc_driver = DataFetcher()

        self.target = {
            'x':                    0.0,
            'y':                    0.0,
            'z':                    0.0,
            'yaw':                  0.0,
        }

        self.channels = {
            'roll':                 1500.0,
            'pitch':                1500.0,
            'throttle':             1000.0,
            'yaw':                  1500.0,
        }

        self.odometry = {
            'position':             (0.0, 0.0, 0.0),
            'orientation':          (0.0, 0.0, 0.0),
            'velocity':             (0.0, 0.0, 0.0),
        }

        self.imu= {
            'gyroscope':            (0.0, 0.0, 0.0),
            'accelerometer':        (0.0, 0.0, 0.0),
        }

        self.altitude = {
            'sonar':                0.0,
            'barometer':            0.0,
        }

        self.optical_flow = {
            'quality':              0.0,
            'flow_rate_x':          0.0,
            'flow_rate_y':          0.0,
            'body_rate_x':          0.0,
            'body_rate_y':          0.0,
        }

        self.flags = {
            'activeSensors':        0,
            'armingDisableFlags':   0,
            'mode':                 0,
        }

        self.approx_koeff = 0.2
        self.alt_expo = None

        self.time_delay = 0.1


    def takeoff(self):
        i = 0
        self.alt_expo = exponential_ramp(remap(self.target['z'], ), )

        self.grpc_driver.get_sonar_data()

        try:
            time.sleep(self.time_delay)
            self.channels['throttle'] = int(self.alt_expo[i])
            if (i + 1) >= len(self.alt_expo):
                return True
            else:
                i += 1
        except Exception as err:
            print("ERR:" + str(err))
            return False

    def land(self):
        i = 0
        self.alt_expo = exponential_ramp(self.channels['throttle'])[::-1]

        self.grpc_driver.get_sonar_data()

        try:
            time.sleep(self.time_delay)
            self.channels['throttle'] = int(self.alt_expo[i])
            if (i + 1) >= len(self.alt_expo):
                return True
            else:
                i += 1
        except Exception as err:
            print("ERR: land error" + str(err))
            return False

    def set_point_to_move(self, x: float, y: float, z: float):
        self.target['x'] = x
        self.target['y'] = y
        self.target['z'] = z

    def move(self):
        grpc_odom = self.grpc_driver.get_odometry_data()
        grpc_att = self.grpc_driver.get_attitude_data()
        self.odometry['position'] = grpc_odom['position']
        self.odometry['velocity'] = grpc_odom['velocity']
        self.odometry['orientation'] = grpc_att['orientation']

        pitch_computed = self.pitch_pid.compute_classic(
            setpoint=self.target['x'],
            value=self.odometry['position'][0]
        )

        roll_computed = self.roll_pid.compute_classic(
            setpoint=self.target['y'],
            value=self.odometry['position'][1]
        )

        yaw_computed = constrain(
            self.yaw_pid.compute_classic(
                setpoint=self.target['yaw'],
                value=self.odometry['orientation'][2]
            ),
            min_val=-2,
            max_val=2
        )

        self.channels['roll'], self.channels['pitch'], self.channels['yaw'] = transform_multirotor_speed(
            roll=self.odometry['orientation'][0],
            pitch=self.odometry['orientation'][1],
            yaw=self.odometry['orientation'][2],
            speed_roll=roll_computed,
            speed_pitch=pitch_computed,
            speed_yaw=yaw_computed
        )

        self.channels['roll'] = 1500 + int(remap(self.channels['roll'], -2, 2, -300, 300))
        self.channels['pitch'] = 1500 + int(remap(self.channels['pitch'], -2, 2, -300, 300))
        self.channels['yaw'] = 1500 + int(remap(self.channels['yaw'], -2, 2, -300, 300))

    def set_velocity(self, vx: float, vy: float, vz: float):
        pass

    def check_desired_altitude(self) -> bool:
        pass

    def check_desired_position(self) -> bool:
        pass

if __name__ == "__main__":
    drone = Drone()
    planner = NavigationMultirotorPlanner(drone)
    while True:
        planner.move()