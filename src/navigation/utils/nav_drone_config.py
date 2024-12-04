from math import radians
from abc import ABC, abstractmethod

# TODO: переработать конфигурационный файл для дрона
# TODO: оформить конфигурационный файл для ARA EDU и ARA FPV


class Drone(ABC):
    roll_rate = 0
    pitch_rate = 0
    yaw_rate = 0

    roll_pitch_expo = 0
    yaw_expo = 0

    max_roll_angle = 0
    max_pitch_angle = 0

    max_altitude = 0
    min_altitude = 0

    max_thrust = 0
    mass = 0

    heading_hold_rate_limit = 0

    pid_gain_p_roll = 0
    pid_gain_i_roll = 0
    pid_gain_d_roll = 0

    pid_gain_p_pitch = 0
    pid_gain_i_pitch = 0
    pid_gain_d_pitch = 0

    pid_gain_p_yaw = 0
    pid_gain_i_yaw = 0
    pid_gain_d_yaw = 0

    pid_gain_p_xy_pos = 0
    pid_gain_p_xy_vel = 0
    pid_gain_i_xy_vel = 0
    pid_gain_d_xy_vel = 0

    pid_gain_p_alt_pos = 0
    pid_gain_p_alt_vel = 0
    pid_gain_i_alt_vel = 0
    pid_gain_d_alt_vel = 0


class ARA_mini():
    roll_rate = radians(400)  # rad per second
    pitch_rate = radians(400)  # rad per second
    yaw_rate = radians(300)  # rad per second

    roll_pitch_expo = 75  # in %
    yaw_expo = 40  # in %

    max_roll_angle = radians(25)
    max_pitch_angle = radians(25)

    max_altitude = 2.3  # in meters
    min_altitude = 0  # in meters

    max_thrust = 150  # gram
    mass = 120  # gram

    heading_hold_rate_limit = radians(40)

    pid_gain_p_roll = 35
    pid_gain_i_roll = 35
    pid_gain_d_roll = 60

    pid_gain_p_pitch = 40
    pid_gain_i_pitch = 40
    pid_gain_d_pitch = 65

    pid_gain_p_yaw = 80
    pid_gain_i_yaw = 45
    pid_gain_d_yaw = 0

    pid_gain_p_xy_pos = 90
    pid_gain_p_xy_vel = 50
    pid_gain_i_xy_vel = 35
    pid_gain_d_xy_vel = 60

    pid_gain_p_alt_pos = 130
    pid_gain_p_alt_vel = 235
    pid_gain_i_alt_vel = 120
    pid_gain_d_alt_vel = 50


class ARA_EDU(Drone):
    roll_rate = radians(400)


class ARA_FPV(Drone):
    roll_rate = radians(400)