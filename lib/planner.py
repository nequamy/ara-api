from lib.pid import PID
from lib.drone import Drone

import numpy as np
from math import e, sin, cos, atan, pi, radians
import time

class Planner():
    def __init__(self, drone: Drone):
        self.roll_pid = PID(5, 3, 3)
        self.pitch_pid = PID(5, 3, 3)
        self.yaw_pid = PID(5, 3, 3)
        
        self.drone = drone
        
        self.target_x = 0
        self.target_y = 0
        self.target_altitude = 0
        self.target_yaw = 0
        
        self.roll = 0
        self.pitch = 0
        self.throttle = 0
        self.yaw = 0
                        
        self.odom = {
            'position':                   [0, 0, 0],
            'velocity':                   [0, 0, 0], 
            'yaw':                         0,
        }
        
        self.rc_channels = 0
    
        self.kp_pos_x = 0.3
        self.kp_pos_y = 0.25
        self.kp_pos_ang_z = 0.1
        self.kp_vel_x = 1.1
        self.kp_vel_y = 1.1
        self.kp_vel_ang_z = 0.05
        
        self.roll_corrected = 0
        self.pitch_corrected = 0
        self.yaw_corrected = 0
        
        self.approx_koef = 0.2
        
        self.upper_threshold = 2000
        self.lower_threshold = 1000
        
        self.orient = 0
        
        self.time_delay = 0.02
        
        self.g = 9.80665
        
    
    def compute(self, odom, att):
        self.odom = odom
        self.orient = att
        
        self.compute_xy()
        self.compute_yaw()
        
        self.transform_speed_to_local()
        # self.throttle = self.compute_throttle()
        
        # return [self.roll, self.pitch, self.throttle, self.yaw]
        
    
    def compute_xy(self):
        dx = self.odom['position'][0] - self.target_x
        dy = self.odom['position'][1] - self.target_y
        
        v_target_x = self.kp_pos_x * dx
        v_target_y = self.kp_pos_y * dy
        
        roll_target = atan((self.kp_vel_y * (v_target_y - self.odom['velocity'][1])) / self.g)
        pitch_target = atan((self.kp_vel_x * (v_target_x - self.odom['velocity'][0])) / self.g)
        
        self.roll_corrected = (roll_target - self.orient.body_rate.y) * self.approx_koef + (1 - self.approx_koef) * self.roll_corrected
        self.pitch_corrected = (pitch_target - self.orient.body_rate.x) * self.approx_koef + (1 - self.approx_koef) * self.pitch_corrected
        
        self.roll = roll_target/ self.drone.max_roll_angle
        self.pitch = pitch_target / self.drone.max_pitch_angle
    
    
    def compute_yaw(self):
        dyaw = self.orient.body_rate.z - self.target_yaw
        dyaw = dyaw - 360 * np.sign(dyaw)
        
        yaw_target = self.kp_pos_ang_z * dyaw
        # yaw_target = self.kp_vel_ang_z * (w_target - self.odom['velocity'][2])
        
        self.yaw = yaw_target
    
    
    def set_point_rel(self, x, y, altitude, yaw):
        self.target_x += x
        self.target_y += y
        self.target_altitude += altitude
        self.target_yaw += radians(yaw)
        self.target_yaw = self.normalize_yaw_radians(self.target_yaw)
    
    def set_point_abs(self, x, y, altitude, yaw):
        self.target_x = x
        self.target_y = y
        self.target_altitude = altitude
        self.target_yaw = radians(yaw)
        self.target_yaw = self.normalize_yaw_radians(self.target_yaw)
        
    def transform_speed_to_local(self):
        roll_rad = self.orient.body_rate.y
        pitch_rad = self.orient.body_rate.x
        yaw_rad = self.orient.body_rate.z
        
        # print(f"Roll:\t{roll_rad}\nPitch:\t{pitch_rad}\nYaw:\t{yaw_rad}")
        
        r_matrix = np.array([
            [
                np.cos(yaw_rad) * np.cos(pitch_rad),
                np.cos(yaw_rad) * np.sin(pitch_rad) * np.sin(roll_rad) - np.sin(yaw_rad) * np.cos(roll_rad),
                np.cos(yaw_rad) * np.sin(pitch_rad) * np.cos(roll_rad) + np.sin(yaw_rad) * np.sin(roll_rad)
            ],
            [
                np.sin(yaw_rad) * np.cos(pitch_rad),
                np.sin(yaw_rad) * np.sin(pitch_rad) * np.sin(roll_rad) + np.cos(yaw_rad) * np.cos(roll_rad),
                np.sin(yaw_rad) * np.sin(pitch_rad) * np.cos(roll_rad) - np.cos(yaw_rad) * np.sin(roll_rad)
            ],
            [
                -np.sin(pitch_rad),
                np.cos(pitch_rad) * np.sin(roll_rad),
                np.cos(pitch_rad) * np.cos(roll_rad)
            ]
        ])
        
        r_transposed = np.transpose(r_matrix)
        
        v_local = np.dot(r_transposed, np.array([self.roll, self.pitch, self.yaw]))
        
        self.rc_channels = np.array([self.speed_to_rc_channel(v_local[0]), 
                                self.speed_to_rc_channel(v_local[1]),
                                1500], dtype=np.int32)
                                # self.speed_to_rc_channel(v_local[2])], dtype=np.int32)
        
        print(self.rc_channels)
        
    
    def speed_to_rc_channel(self, speed, channel_center=1500, channel_range=500):
        pid_output = np.clip(speed, -1, 1) * channel_range
        return channel_center + pid_output
        
        
    def normalize_yaw_radians(self, yaw):
        """
        Нормализует угол по yaw в радианах в диапазоне от 0 до 2π радиан.
        
        Args:
        yaw (float): Угол по yaw в радианах.
        
        Returns:
        float: Нормализованный угол по yaw в диапазоне от 0 до 2π радиан.
        """
        normalized_yaw = (yaw + 2 * np.pi) % (2 * np.pi)
    
        return normalized_yaw
        
    def exponential_ramp(self, target_value: float = 0, delay: float = 0):
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
        
        num_steps = (target_value / delay) * e
        
        k = np.log(target_value / self.lower_threshold) / (num_steps - 1)
        values = self.lower_threshold * np.exp(k * np.arange(num_steps))
        
        values = np.int32(np.minimum(values, self.upper_threshold))
        
        return values
    
    def check_desired_position(self) -> bool:
        
        if (self.target_x - 0.1) < self.odom['position'][0] < (self.target_x + 0.1):
            if self.target_y - 0.1 < self.odom['position'][1] < self.target_y + 0.1:
                if self.target_altitude - 0.1 < self.odom['position'][2] < self.target_altitude + 0.1:
                    if self.target_yaw - 0.1 < self.orient.body_rate.z < self.target_yaw + 0.1:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    
    def remap(self, x):
        return (x - self.drone.min_altitude) * (self.upper_threshold - self.lower_threshold) / (self.drone.max_altitude - self.drone.min_altitude) + self.lower_threshold