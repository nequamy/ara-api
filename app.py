from lib.api_driver import MultirotorControl
from lib.transmitter import UDPTransmitter, TCPTransmitter

import pandas as pd
import numpy as np
from math import atan2, sqrt, radians
import time

from data.altitude import Altitude
from data.attitude import Attitude
from data.barometer import Barometer
from data.battery import Battery
from data.channels import Channels
from data.flags import Flags
from data.odom import Odometry
from data.imu import Imu


class Api(object):
    def __init__(self, ip: str, port: int):
        self.connector = TCPTransmitter((ip, port))
        print("AAAAA")
        self.driver = MultirotorControl(self.connector)
        print("AAAAA")
        self.driver.connect()
        print("AAAAA")

        self.altitude = Altitude()
        self.attitude = Attitude()
        self.barometer = Barometer()
        self.battery = Battery()
        self.channels = Channels()
        self.flags = Flags()
        self.odom = Odometry()
        self.imu = Imu()
        
        self.is_armed = False
        self.airmode = False
        
        self.roll_acc = 0
        self.pitch_acc = 0
        self.roll_rate = 0
        self.pitch_rate = 0
        self.roll = 0
        self.pitch = 0 
        self.yaw = 0
        
        self.dt = 0.1
        
        self.Kp = 0.5
        self.Ki = 0.1

        
    def update_loop(self) -> None:
        while True:
            self.update_data()

            self.load_data()

    def update_data(self) -> None:
        self.update_imu()
        # self.update_battery()
        self.update_attitude()
        self.update_rc_in()
        self.update_odometry()
        time.sleep(0.05)

    def load_data(self) -> None:
        # self.cmd_send(None)
        pass

    def takeoff(self, altitude: int = None) -> bool:
        return self.exec(cmd="takeoff", z=altitude)

    def navigate(self, x: float = None, y: float = None, z: float = None) -> bool:
        return self.exec(cmd="navigate", x=x, y=y)

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

        print(f"IMU:\t X - \t{self.imu.angular_velocity.x}\tY - \t{self.imu.angular_velocity.y}\tZ - \t{self.imu.angular_velocity.z}")

    def update_altitude(self):
        """
        Function for publishing altitude values from barometer and rangefinder from FC

        publish: eagle_eye_msgs/Altitude
        """

        self.driver.fast_read_altitude()
        self.altitude.monotonic = self.driver.SENSOR_DATA['altitude']
        self.altitude.relative = float(self.driver.SENSOR_DATA['sonar'])
        self.barometer.altitude = float(self.driver.SENSOR_DATA['sonar'])
        
        print(f"Altitude:\tBaro - \t{self.barometer.altitude}\tSonar - \t{self.altitude.relative}\tMonotonic - \t{self.altitude.monotonic}")

    def update_battery(self):
        """
        Function for publishing system voltage from FC

        publish: eagle_eye_msgs/Battery
        """
        self.driver.fast_read_analog()
        # self.battery.voltage = round(self.driver.ANALOG['voltage'], 2)
        # self.battery.amperage = round(self.driver.ANALOG['amperage'], 2)
        # self.battery.mah = float(self.driver.ANALOG['mAhdrawn'])
        # self.battery.count_of_cells = f"{int(self.driver.ANALOG['voltage'] / 3.7)}s"
        # self.battery.percent_of_voltage = int(self.battery.voltage / (4.2 * self.driver.ANALOG['voltage'] / 3.7) * 100)
        
    def update_odometry(self):
        """
        Function for publishing optical flow values.
        
        

        publish: eagle_eye_msgs/OpticalFlow
        """
        self.odom = self.driver.fast_read_odom()
        # print(type(self.odom))
        print(f"Odom:\tX - \t{self.odom['position'][0]}\tY - \t{self.odom['position'][1]}\tZ - \t{self.odom['position'][2]}")
        
    def update_attitude(self):
        """
        Function for publishing more accurate orientation
        based on complementary filter from FC (heading)

        publish: eagle_eye_msgs/Attitude
        """
        self.driver.fast_read_attitude()

        self.ang_x = radians(self.driver.SENSOR_DATA['kinematics'][0])
        self.ang_y = radians(self.driver.SENSOR_DATA['kinematics'][1])
        self.ang_z = -1 * radians(self.driver.SENSOR_DATA['kinematics'][2])

        print(f"Attitude:\tX - \t{self.ang_x}\tY - \t{self.ang_y}\tZ - \t{self.ang_z}")
        
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
        
    def cmd_send(self, data):
        """
        Function for sending values on RC channels to FC via MSP protocol

        publish: eagle_eye_msgs/Channels
        """
        if data.linear.x is not None and not np.isnan(data.linear.x):
            pitch = self.constrain(int(1500 + data.linear.x * 100), 250)
        else:
            pitch = 1500
            print("CMD LINEAR X IS NONE")
        if data.linear.y is not None and not np.isnan(data.linear.y):
            roll = self.constrain(int(1500 - data.linear.y * 100), 250)
        else:
            roll = 1500
            print("CMD LINEAR Y IS NONE")
        if data.angular.z is not None and not np.isnan(data.angular.z):
            yaw = self.constrain(int(1500 - data.angular.z * 100), 250)
        else:
            yaw = 1500
            print("CMD ANGULAR Z IS NONE")
        trust = 1500
        arm = 1600
        
        self.data = [roll, pitch, trust, yaw, arm, 2000, 0, 0]
        
        self.driver.fast_msp_rc_cmd(self.data)

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
        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        
        return [qx, qy, qz, qw]
        