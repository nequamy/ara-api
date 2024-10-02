from lib.api_driver import MultirotorControl
from lib.transmitter import UDPTransmitter, TCPTransmitter
from lib.drone import Drone
from lib.planner import Planner
from lib.pid import PID

import numpy as np
from math import atan2, sqrt, radians
from threading import Thread
import time

import colorama
from colorama import Fore
import pyfiglet

from data.altitude import Altitude
from data.attitude import Attitude
from data.barometer import Barometer
from data.battery import Battery
from data.channels import Channels
from data.flags import Flags
from data.odom import Odometry
from data.imu import Imu


class Api(object):
    def __init__(self, ip: str, port: int, drone: Drone):

        colorama.init()

        ascii_art = pyfiglet.figlet_format("ARA MINI API v1", font="slant", width=50)
        summary = ("Поздравляем! Вы запустили API для программирования ARA MINI\n\n"
                   "Для подключения в конфигуратеоре:\n"
                   "\tUDP: \thttp://192.168.2.1:14550\n"
                   "\tTCP: \thttp://192.168.2.1:5760\n\n"
                   "Изображение с камеры: \t\thttp://192.168.2.113:81/stream\n")
        print(Fore.BLUE + ascii_art)
        print("=" * 60)
        print(Fore.CYAN + summary)

        print(Fore.RED + "Data output:")
        print(Fore.MAGENTA)
        colorama.deinit()

        self.connector = TCPTransmitter((ip, port))
        self.driver = MultirotorControl(self.connector)
        self.driver.connect()

        self.drone = drone
        self.drone_planner = Planner(drone)

        self.attitude = Attitude()
        self.battery = Battery()
        self.channels = Channels()
        self.rc_out = Channels()
        self.odom = {
            'position': [0, 0, 0],
            'velocity': [0, 0, 0],
            'yaw': 0,
        }
        self.odom_zero = {
            'position': [0, 0, 0],
            'velocity': [0, 0, 0],
            'yaw': 0,
        }
        self.imu = Imu()

        self.is_armed = False
        self.airmode = False

        self.arm_state = 0
        self.nav_state = 0

        self.roll_acc = 0
        self.pitch_acc = 0
        self.roll_rate = 0
        self.pitch_rate = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

        self.ang_x = 0
        self.ang_y = 0
        self.ang_z = 0
        self.ang_x_zero = 0
        self.ang_y_zero = 0
        self.ang_z_zero = 0

        self.odom_zero_flag = True
        self.att_zero_flag = True

        self.alt_pid = PID(5, 3, 3)

        self.dt = 0.1

        self.Kp = 0.5
        self.Ki = 0.1

        self.time_delay = 0.5

    def update_loop(self) -> None:
        while True:
            # print(self.rc_out.channels)
            self.update_data()

            self.load_data()

    def update_data(self) -> None:
        self.update_imu()
        self.update_attitude()
        self.update_rc_in()
        self.update_odometry()
        self.drone_planner.set_attitude(self.attitude)

    def load_data(self) -> None:
        self.rc_out.channels[0] = self.drone_planner.roll_corrected
        self.rc_out.channels[1] = self.drone_planner.pitch_corrected
        self.rc_out.channels[2] = self.drone_planner.throttle
        self.rc_out.channels[3] = 1500
        self.rc_out.channels[4] = (self.arm_state * 1000) + 1000
        self.rc_out.channels[6] = (self.nav_state * 500) + 1000

        print(f"RC:\t{self.rc_out.channels[0:8]}\nOdom:\n\tX - \t{self.odom['position'][0]}\n\tY - \t{self.odom['position'][1]}\n\tZ - \t{self.odom['position'][2]}\n"
              f"Angle X:\t{self.attitude.body_rate.x}\nAngle Y:\t{self.attitude.body_rate.y}\nAngle Z:\t{self.attitude.body_rate.z}\n")

        self.cmd_send()

    def set_arm_state(self, state: bool = 0) -> bool:
        self.arm_state = int(state)
        return True

    def set_nav_state(self, state: int = 0) -> bool:
        if state > 2:
            print("ERR: invalid navigation state value")
            return False

        self.nav_state = state
        return True

    def set_velocity_throttle(self, throttle: int | float = 0) -> bool:
        return self.drone_planner.set_throttle(throttle)

    def set_velocity_x(self, x_vel: int | float = 0) -> bool:
        return self.drone_planner.set_vel_x(x_vel)

    def set_velocity_y(self, y_vel: int | float = 0) -> bool:
        return self.drone_planner.set_vel_y(y_vel)

    def takeoff(self, altitude: int | float = None) -> bool:
        if altitude is None:
            print("ERR: set altitude for takeoff method")
            self.reset_state()
            return False

        if self.drone.max_altitude < altitude:
            print("ERR: out of bounds altitude")
            self.reset_state()
            return False

        self.drone_planner.set_point(altitude=altitude)

        if self.drone_planner.takeoff():
            return True
        else:
            self.reset_state()
            return False

    def land(self, auto_disarm: bool = 0) -> bool:
        self.drone_planner.set_point(altitude=0)

        if self.drone_planner.land():
            self.arm_state = not auto_disarm
            return True
        else:
            self.reset_state()
            return False

    def go_to_xy(self, x: float = None, y: float = None,
                 auto_land: bool = False) -> bool:
        self.drone_planner.set_point(x=x, y=y)
        self.drone_planner.set_attitude(self.attitude)

        while not self.drone_planner.check_desired_position():
            self.drone_planner.compute(self.odom, self.attitude)

        self.drone_planner.roll_corrected = 1500
        self.drone_planner.pitch_corrected = 1500

        time.sleep(5)

        if auto_land:
            self.land(auto_disarm=True)

        return True

    def update_imu(self):
        """
        Function for publishing accelerometer, gyroscope and drone orientation values

        publish: sensor_msgs/Imu
        """

        self.driver.fast_read_imu()
        self.imu.linear_acceleration.x = self.driver.SENSOR_DATA['accelerometer'][0]
        self.imu.linear_acceleration.y = self.driver.SENSOR_DATA['accelerometer'][1]
        self.imu.linear_acceleration.z = self.driver.SENSOR_DATA['accelerometer'][2]

        self.imu.angular_velocity.x = self.driver.SENSOR_DATA['gyroscope'][0]
        self.imu.angular_velocity.y = self.driver.SENSOR_DATA['gyroscope'][1]
        self.imu.angular_velocity.z = self.driver.SENSOR_DATA['gyroscope'][2]

        self.roll_acc = atan2(self.imu.linear_acceleration.y, self.imu.linear_acceleration.z)
        self.pitch_acc = atan2(-self.imu.linear_acceleration.x,
                               sqrt(self.imu.linear_acceleration.y * self.imu.linear_acceleration.y
                                    + self.imu.linear_acceleration.z * self.imu.linear_acceleration.z))

        self.roll_rate = self.driver.SENSOR_DATA['gyroscope'][0]
        self.pitch_rate = self.driver.SENSOR_DATA['gyroscope'][1]
        self.yaw_rate = self.driver.SENSOR_DATA['gyroscope'][2]

        self.roll += self.dt * (self.roll_rate - self.Kp * self.roll_acc + self.Ki * self.roll)
        self.pitch += self.dt * (self.pitch_rate - self.Kp * self.pitch_acc + self.Ki * self.pitch)
        self.yaw += self.dt * self.yaw_rate

        quat = self.euler_to_quaternion(self.roll, self.pitch, self.yaw)

        self.imu.orientation.x = quat[0]
        self.imu.orientation.y = quat[1]
        self.imu.orientation.z = quat[2]
        self.imu.orientation.w = quat[3]

    def update_altitude(self):
        """
        Function for publishing altitude values from barometer and rangefinder from FC

        publish: eagle_eye_msgs/Altitude
        """

        self.driver.fast_read_altitude()
        self.altitude.monotonic = self.driver.SENSOR_DATA['altitude']
        self.altitude.relative = float(self.driver.SENSOR_DATA['sonar'])
        self.barometer.altitude = float(self.driver.SENSOR_DATA['sonar'])

    def update_odometry(self):
        """
        Function for publishing optical flow values.

        publish: eagle_eye_msgs/OpticalFlow
        """
        self.odom = self.driver.fast_read_odom()

        if self.odom_zero_flag:
            self.odom_zero['position'][0] = self.odom['position'][0]
            self.odom_zero['position'][1] = self.odom['position'][1]
            self.odom_zero['position'][2] = self.odom['position'][2]
            self.odom_zero['yaw'] = self.odom['yaw']
            self.odom_zero_flag = False

        self.odom['position'][0] = -round(self.odom['position'][0] - self.odom_zero['position'][0], 2)
        self.odom['position'][1] = round(self.odom['position'][1] - self.odom_zero['position'][1], 2)
        self.odom['position'][2] = round(self.odom['position'][2] - self.odom_zero['position'][2], 2)
        self.odom['yaw'] = self.odom['yaw'] - self.odom_zero['yaw']

    def update_attitude(self):
        """
        Function for publishing more accurate orientation
        based on complementary filter from FC (heading)

        publish: eagle_eye_msgs/Attitude
        """
        self.driver.fast_read_attitude()

        if self.att_zero_flag:
            self.ang_x_zero = radians(self.driver.SENSOR_DATA['kinematics'][0])
            self.ang_y_zero = radians(self.driver.SENSOR_DATA['kinematics'][1])
            self.ang_z_zero = radians(self.driver.SENSOR_DATA['kinematics'][2])
            self.att_zero_flag = False

        self.ang_x = radians(self.driver.SENSOR_DATA['kinematics'][0]) - self.ang_x_zero
        self.ang_y = radians(self.driver.SENSOR_DATA['kinematics'][1]) - self.ang_y_zero
        self.ang_z = radians(self.driver.SENSOR_DATA['kinematics'][2]) - self.ang_z_zero

        self.attitude.body_rate.x = self.ang_x
        self.attitude.body_rate.y = self.ang_y
        self.attitude.body_rate.z = self.ang_z

        quat = self.euler_to_quaternion(self.ang_x, self.ang_y, self.ang_z)

        self.attitude.orientation.x = quat[0]
        self.attitude.orientation.y = quat[1]
        self.attitude.orientation.z = quat[2]
        self.attitude.orientation.w = quat[3]

    def update_basic(self):
        """
        Function for publishing information about flags inside FC

        int32 cycle_time - time of one FC iteration; \n
        int32 cpuload - FC CPU load (in percent); \n
        int32 arming_disable_count - disable count of arming; \n

        string[] arming_disable_flags - flags of internal FC errors; \n
        string[] active_sensors - enabled sensors (not only working ones); \n
        string[] mode - current modes of the flyer. \n

        publish: eagle_eye_msgs/Flags
        """
        self.driver.fast_read_status()

        self.flags.cycle_time = self.driver.CONFIG['cycleTime']
        self.flags.arming_disable_count = self.driver.CONFIG['armingDisableCount']

        self.flags.arming_disable_flags = self.finder(self.driver.CONFIG['armingDisableFlags'],
                                                      self.driver.armingCheckFlags_INAV)
        self.flags.active_sensors = self.finder(self.driver.CONFIG['activeSensors'],
                                                self.driver.sensorsCheckFlags_INAV)
        self.flags.mode = self.finder(int(self.driver.CONFIG['mode'] / 8),
                                      self.driver.modesCheckFlags_INAV)

    def update_rc_in(self):
        """
        Function for reading RC channels coming from the remote driver unit

        publish: eagle_eye_msgs/Channels
        """
        self.driver.fast_read_rc_channels()
        self.channels.channels = self.driver.RC['channels']

    def cmd_send(self):
        """
        Function for sending values on RC channels to FC via MSP protocol

        publish: eagle_eye_msgs/Channels
        """
        self.rc_out.channels[7] = 2000
        self.driver.fast_msp_rc_cmd(self.rc_out.channels)

    @staticmethod
    def finder(flags: int, dict_flags: dict):
        """
        Function to search for matching byte flags in the dictionary

        :rtype: String[]
        :return: string array of matches with flags
        """
        msg = []
        for k, v in dict_flags.items():
            if int(flags) & v:
                msg.append(k)
        return msg

    def euler_to_quaternion(self, roll, pitch, yaw):
        qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(
            yaw / 2)
        qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(
            yaw / 2)
        qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(
            yaw / 2)
        qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(
            yaw / 2)

        return [qx, qy, qz, qw]

    def reset_state(self):
        self.arm_state = 0
        self.nav_state = 0

    def check_desired_alt(self, altitude: float = 0) -> bool:
        if altitude - 0.05 < self.odom['position'][2] < altitude + 0.05:
            return True
        else:
            return False
