from datetime import datetime
import time
import logging
import os


class PID(object):
    """
    PID Controller

    This class implements a PID controller with three different computation methods:
    classic, windup, and feedforward.

    Attributes:
        kp (float): Proportional gain.
        ki (float): Integral gain.
        kd (float): Derivative gain.
        name (str): Name of the PID controller for logging purposes.
    """

    def __init__(self, kp: float = 0, ki: float = 0, kd: float = 0, name: str = "PID"):
        """
        Initializes the PID controller with the given gains and name.

        Args:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
            name (str): Name of the PID controller.
        """
        self.windup_guard = 1
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

        self.name = name
        self.__init_logging__()

    def __init_logging__(self, log_directory='log/pids'):
        """
        Initializes the logging for the PID controller.

        Args:
            log_directory (str): Directory where the log files will be stored.
        """
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_name = f"{self.name}_pid_works_{timestamp}.log"

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler = logging.FileHandler(os.path.join(log_directory, log_file_name))
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def compute_classic(self, setpoint, value):
        """
        Computes the PID output using the classic PID formula.

        Args:
            setpoint (float): The desired value.
            value (float): The current value.

        Returns:
            float: The computed PID output.
        """
        self.curr_time = time.time() if self.curr_time is None else self.curr_time
        self.err = setpoint - value

        self.dt = (self.curr_time - self.prev_time) if (self.curr_time - self.prev_time) > 0 else 0.1

        self.p_term = self.err * self.kp
        self.i_term += self.err * self.dt
        self.d_term = (self.err - self.prev_err) / (self.dt * 1000)
        self.prev_time = self.curr_time
        self.curr_time = time.time()

        self.pid = self.p_term + self.ki * self.i_term + self.d_term * self.kd

        self.constrain(-2, 2)

        self.smoothed_pid = self.alpha * self.pid + (1 - self.alpha) * self.smoothed_pid

        self.logger.info(f'PID: {self.pid}, Error: {self.err}, P: {self.p_term}, I: {self.i_term}, D: {self.d_term}')

        return self.smoothed_pid

    def compute_windup(self, setpoint, value):
        """
        Computes the PID output using the windup guard to prevent integral windup.

        Args:
            setpoint (float): The desired value.
            value (float): The current value.

        Returns:
            float: The computed PID output.

        """
        self.curr_time = time.time() if self.curr_time is None else self.curr_time
        self.err = setpoint - value

        self.dt = (self.curr_time - self.prev_time) if (self.curr_time - self.prev_time) > 0 else 0.1

        self.p_term = self.err * self.kp
        self.i_term += self.err * self.dt

        self.i_term = self.constrain(self.i_term, -self.windup_guard, self.windup_guard)

        self.d_term = (self.err - self.prev_err) / (self.dt * 1000)
        self.prev_time = self.curr_time
        self.curr_time = time.time()

        self.pid = self.p_term + self.ki * self.i_term + self.d_term * self.kd

        self.smoothed_pid = self.alpha * self.pid + (1 - self.alpha) * self.smoothed_pid

        self.logger.info(f'PID: {self.pid}, Error: {self.err}, P: {self.p_term}, I: {self.i_term}, D: {self.d_term}')

        return self.smoothed_pid

    def compute_feedforward(self, setpoint, value):
        """
        Computes the PID output with an additional feedforward term.

        Args:
            setpoint (float): The desired value.
            value (float): The current value.

        Returns:
            float: The computed PID output.
        """
        self.curr_time = time.time() if self.curr_time is None else self.curr_time
        self.err = setpoint - value

        self.dt = (self.curr_time - self.prev_time) if (self.curr_time - self.prev_time) > 0 else 0.1

        self.p_term = self.err * self.kp
        self.i_term += self.err * self.dt
        self.d_term = (self.err - self.prev_err) / (self.dt * 1000)
        self.prev_time = self.curr_time
        self.curr_time = time.time()

        feedforward_term = setpoint * self.kp

        self.pid = self.p_term + self.ki * self.i_term + self.d_term * self.kd + feedforward_term

        self.smoothed_pid = self.alpha * self.pid + (1 - self.alpha) * self.smoothed_pid

        self.logger.info(
            f'PID: {self.pid}, Error: {self.err}, P: {self.p_term}, I: {self.i_term}, D: {self.d_term}, Feedforward: {feedforward_term}')

        return self.smoothed_pid

    def set_kp(self, proportional_gain):
        """
        Sets the proportional gain.

        Args:
            proportional_gain (float): The new proportional gain.
        """
        self.kp = proportional_gain

    def set_ki(self, integral_gain):
        """
        Sets the integral gain.

        Args:
            integral_gain (float): The new integral gain.
        """
        self.ki = integral_gain

    def set_kd(self, derivative_gain):
        """
        Sets the derivative gain.

        Args:
            derivative_gain (float): The new derivative gain.
        """
        self.kd = derivative_gain

    def constrain(self, max_value: float, min_value: float) -> float:
        """
        Constrains the PID output to be within the given range.

        Args:
            max_value (float): The maximum value.
            min_value (float): The minimum value.

        Returns:
            float: The constrained PID output.
        """
        if self.pid > max_value:
            return max_value
        elif self.pid < min_value:
            return min_value
        else:
            return self.pid