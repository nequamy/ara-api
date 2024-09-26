from math import radians
from abc import ABC, abstractmethod

class Drone(ABC):
    @abstractmethod
    def __init__(self):
        self.roll_rate = 0
        self.pitch_rate = 0
        self.yaw_rate = 0
        
        self.roll_pitch_expo = 0
        self.yaw_expo = 0
        
        self.max_roll_angle = 0
        self.max_pitch_angle = 0
        
        self.max_altitude = 0
        self.min_altitude = 0
        
        self.heading_hold_rate_limit = 0
        
        self.pid_gain_p_roll = 0
        self.pid_gain_i_roll = 0
        self.pid_gain_d_roll = 0
        
        self.pid_gain_p_pitch = 0
        self.pid_gain_i_pitch = 0
        self.pid_gain_d_pitch = 0
        
        self.pid_gain_p_yaw = 0
        self.pid_gain_i_yaw = 0
        self.pid_gain_d_yaw = 0
        
        self.pid_gain_p_xy_pos = 0
        self.pid_gain_p_xy_vel = 0
        self.pid_gain_i_xy_vel = 0
        self.pid_gain_d_xy_vel = 0
        
        self.pid_gain_p_alt_pos = 0
        self.pid_gain_p_alt_vel = 0
        self.pid_gain_i_alt_vel = 0
        self.pid_gain_d_alt_vel = 0

class ARA_mini():
    def __init__(self):
        self.roll_rate = radians(400) # rad per second
        self.pitch_rate = radians(400) # rad per second
        self.yaw_rate = radians(300) # rad per second
        
        self.roll_pitch_expo = 75 # in %
        self.yaw_expo = 40 # in %
        
        self.max_roll_angle = radians(25) 
        self.max_pitch_angle = radians(25)
        
        self.max_altitude = 3 # in meters
        self.min_altitude = 0 # in meters
        
        self.heading_hold_rate_limit = radians(40)
        
        self.pid_gain_p_roll = 35
        self.pid_gain_i_roll = 35
        self.pid_gain_d_roll = 60
        
        self.pid_gain_p_pitch = 40
        self.pid_gain_i_pitch = 40
        self.pid_gain_d_pitch = 65
        
        self.pid_gain_p_yaw = 80
        self.pid_gain_i_yaw = 45
        self.pid_gain_d_yaw = 0
        
        self.pid_gain_p_xy_pos = 90
        self.pid_gain_p_xy_vel = 50
        self.pid_gain_i_xy_vel = 35
        self.pid_gain_d_xy_vel = 60
        
        self.pid_gain_p_alt_pos = 130
        self.pid_gain_p_alt_vel = 235
        self.pid_gain_i_alt_vel = 120
        self.pid_gain_d_alt_vel = 50