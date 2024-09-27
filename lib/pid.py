import time


class PID(object):
    def __init__(self, kp: float = 0, ki: float = 0, kd: float = 0):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.err = 0
        
        self.p_term = 0
        self.i_term = 0
        self.d_term = 0
        
        self.pid = 0
        self.smoothed_pid = 0
        self.alpha = 0.2

        self.dt = 0.1
        
        self.prev_err = 0
        
        self.curr_time = None
        self.prev_time = time.time()

    def compute(self, setpoint, value):
        self.curr_time = time.time() if self.curr_time == None else self.curr_time
        self.err = setpoint - value
        
        self.dt = ((self.curr_time - self.prev_time)) if (self.curr_time - self.prev_time) > 0 else 0.1
        
        self.p_term = self.err * self.kp
        # self.i_term += self.err * self.dt
        self.d_term = (self.err - self.prev_err) / (self.dt * 1000)
        self.prev_time = self.curr_time
        self.curr_time = time.time()
        
        # print(f"Pterm:\t{self.p_term}\nIterm:\t{self.i_term}\nDterm:\t{self.d_term}")
        self.pid = self.p_term + self.ki * self.i_term + self.d_term * self.kd

        self.constrain(-2, 2)

        self.smoothed_pid = self.alpha * self.pid + (1 - self.alpha) * self.smoothed_pid
        
        return self.smoothed_pid

    def set_kp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.kp = proportional_gain

    def set_ki(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.ki = integral_gain

    def set_kd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.kd = derivative_gain

    def constrain(self, max_value: float, min_value: float) -> float:
        if self.pid > max_value:
            return max_value
        elif self.pid < min_value:
            return min_value
        else:
            return self.pid
        
