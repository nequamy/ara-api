import math

from lib.pid import PID
from lib.drone import Drone

import numpy as np
from math import e, sin, cos, atan, pi, radians
import time


class Planner():
    def __init__(self, drone: Drone):
        self.alt_expo = [0]
        self.roll_pid = PID(kp=2.5, kd=1.5)
        self.pitch_pid = PID(kp=2.5, kd=1.5)
        self.yaw_pid = PID(kp=3, kd=1)

        self.drone = drone

        self.target_x = 0
        self.target_y = 0
        self.target_altitude = 0
        self.target_yaw = 0

        self.roll = 0
        self.pitch = 0
        self.throttle = 1000
        self.yaw = 0

        self.odom = {
            'position': [0, 0, 0],
            'velocity': [0, 0, 0],
            'yaw': 0,
        }

        self.rc_channels = 0

        self.roll_corrected = 1500
        self.pitch_corrected = 1500
        self.yaw_corrected = 1500

        self.approx_koef = 0.2

        self.upper_threshold = 2000
        self.lower_threshold = 1000

        self.orient = 0

        self.time_delay = 0.4

        self.g = 9.80665

    def compute(self, odom, att):
        self.odom = odom
        self.orient = att

        self.compute_xy()
        self.compute_yaw()

        # self.pitch = 1
        # self.roll = 0

        self.transform_speed_to_local()

        # print(self.roll, self.pitch, self.yaw)

        # self.throttle = self.compute_throttle()

        self.roll_corrected = 1500 + int(self.remap_by_max_min(self.roll, -2, 2, -300, 300))
        self.pitch_corrected = 1500 + int(self.remap_by_max_min(self.pitch, -2, 2, -300, 300))
        self.yaw_corrected = 1500 + int(self.remap_by_max_min(self.yaw, -2, 2, -300, 300))

    def compute_xy(self):
        self.pitch = self.pitch_pid.compute(self.target_x, self.odom['position'][0])
        self.roll = self.roll_pid.compute(self.target_y, self.odom['position'][1])

    def compute_yaw(self):
        # print(f"yaw:\t{self.odom['yaw']}, \ttarget:\t{self.target_yaw}")
        self.yaw = self.yaw_pid.compute(self.target_yaw, self.odom['yaw'])
        self.yaw = self.constrain(self.yaw, -2, 2)
        # print(f"yaw velocity:\t{self.yaw}")

    def takeoff(self):
        i = 0
        self.alt_expo = self.exponential_ramp(self.remap(self.target_altitude))

        while not self.check_desired_altitude():
            try:
                time.sleep(self.time_delay)
                self.throttle = int(self.alt_expo[i])
                if (i + 1) >= len(self.alt_expo):
                    continue
                else:
                    i += 1
            except Exception as err:
                print("ERR:" + str(err))
                return False

        return True

    def land(self):
        i = 0
        alt_expo = self.exponential_ramp(self.throttle)[::-1]
        while self.check_desired_altitude(0):
            try:
                time.sleep(self.time_delay)
                self.throttle = int(alt_expo[i])
                if (i + 1) >= len(alt_expo):
                    continue
                else:
                    i += 1
            except Exception as err:
                print("ERR: land error" + str(err))
                return False

        return True

    def set_point(self, x: int | float = None, y: int | float = None,
                      altitude: int | float = None, yaw: int | float = None):
        if x is not None:
            self.target_x = x
        if y is not None:
            self.target_y = y
        if altitude is not None:
            self.target_altitude = altitude
        if yaw is not None:
            self.target_yaw = radians(yaw)
            self.target_yaw = self.normalize_radians(self.target_yaw)

    def set_attitude(self, attitude):
        self.orient = attitude

    def transform_speed_to_local(self):
        roll_rad = self.normalize_radians(self.orient.body_rate.y)
        pitch_rad = self.normalize_radians(self.orient.body_rate.x)
        yaw_rad = self.normalize_radians(self.orient.body_rate.z)

        # print(f"Roll:\t{roll_rad}\nPitch:\t{pitch_rad}\nYaw:\t{yaw_rad}")
        syaw = sin(yaw_rad)
        cyaw = cos(yaw_rad)

        spitch = sin(pitch_rad)
        cpitch = cos(pitch_rad)

        sroll = sin(roll_rad)
        croll = cos(roll_rad)

        r_matrix = np.array([
            [
                cyaw * cpitch,
                cyaw * spitch * sroll - syaw * croll,
                cyaw * spitch * croll + syaw * sroll
            ],
            [
                syaw * cpitch,
                syaw * spitch * sroll + cyaw * croll,
                syaw * spitch * croll - cyaw * sroll
            ],
            [
                -spitch,
                cpitch * sroll,
                cpitch * croll
            ]
        ])

        r_transposed = np.transpose(r_matrix)

        v_local = r_transposed @ np.array([self.roll, self.pitch, self.yaw])

        self.roll = self.constrain(v_local[0], -2, 2)
        self.pitch = self.constrain(v_local[1], -2, 2)

    def normalize_radians(self, angle):
        """
        Нормализует угол по yaw в радианах в диапазоне от 0 до 2π радиан.
        
        Args:
        yaw (float): Угол по yaw в радианах.
        
        Returns:
        float: Нормализованный угол по yaw в диапазоне от 0 до 2π радиан.
        """
        normalized_yaw = (angle + 2 * np.pi) % (2 * np.pi)

        return normalized_yaw

    def exponential_ramp(self, target_value: float = 0):
        """
        Создает массив чисел, плавно увеличивающихся от минимального значения до целевого значения по экспоненциальной кривой,
        но не превышающих максимальное значение.
        
        Args:
        target_value (float): Целевое значение.
        num_steps (int): Количество шагов для вычисления массива.
        
        Returns:
        numpy.ndarray: Массив значений.
        """
        target_value = min(target_value, self.upper_threshold)

        num_steps = (target_value / 200) * e

        k = np.log(target_value / self.lower_threshold) / (num_steps - 1)
        values = self.lower_threshold * np.exp(k * np.arange(num_steps))

        values = np.int32(np.minimum(values, self.upper_threshold))

        return values

    def check_desired_xyzy(self):
        # print(f"YAW: \t{self.check_desired_yaw()}")
        # print(f"POS: \t{self.check_desired_position()}\n")
        return self.check_desired_yaw() and self.check_desired_position()

    def check_desired_yaw(self) -> bool:
        if self.target_yaw - 0.1 < self.orient.body_rate.z < self.target_yaw + 0.1:
            return True
        else:
            return False

    def check_desired_altitude(self, alt: int = None) -> bool:
        if alt is None:
            check_alt = self.alt_expo[len(self.alt_expo) - 1]
        else:
            check_alt = 1000 + 500 * alt

        if self.throttle == check_alt:
            return True
        else:
            return False

    def check_desired_position(self) -> bool:
        if (self.target_x - 0.12) < self.odom['position'][0] < (self.target_x + 0.12):
            if self.target_y - 0.12 < self.odom['position'][1] < self.target_y + 0.12:
                return True
            else:
                return False
        else:
            return False

    def remap(self, x):
        return (x - self.drone.min_altitude) * (self.upper_threshold - self.lower_threshold) / (
                self.drone.max_altitude - self.drone.min_altitude) + self.lower_threshold

    def remap_by_max_min(self, x, min_old, max_old, min_new, max_new):
        return (x - min_old) * (max_new - min_new) / (max_old - min_old) + min_new

    def constrain(self, val, min_val, max_val):
        return min(max_val, max(min_val, val))
