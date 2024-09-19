import time


class PID(object):
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.p_term = 0
        self.i_term = 0
        self.d_term = 0
        
        self.prev_err = 0
        
        self.curr_time = time.time()
        self.prev_time = 0

    def compute(self, setpoint, value) -> type(setpoint):
        err = setpoint - value
        
        self.p_term = err * self.kp
        self.i_term += (self.dt * self.err) / self.ki
        self.d_term = (self.err - self.prev_err) / ((self.curr_time - self.prev_time) * 1000)
        self.prev_time = self.curr_time
        self.curr_time = time.time()
        
        return self.p_term + self.i_term + self.d_term

    @staticmethod
    def constrain(self, value: any, max_value: float, min_value: float) -> float:
        if value > max_value:
            return max_value
        elif value < min_value:
            return min_value
        else:
            return value
        
    def set_kp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.kp = proportional_gain

    def set_ki(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.ki = integral_gain

    def set_kd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.kd = derivative_gain
