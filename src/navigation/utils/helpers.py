import logging
import os
from math import sin, cos, e
import numpy as np
import grpc
import protos.api_pb2 as api_pb2
import protos.api_pb2_grpc as api_pb2_grpc



def transform_multirotor_speed(roll, pitch, yaw, speed_roll, speed_pitch, speed_yaw):
    syaw = sin(yaw)
    cyaw = cos(yaw)

    spitch = sin(pitch)
    cpitch = cos(pitch)

    sroll = sin(roll)
    croll = cos(roll)

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

    v_local = np.matmul(r_transposed, np.array([speed_roll, speed_pitch, speed_yaw]))

    return (constrain(v_local[0], -2, 2), # roll velocity
            constrain(v_local[1], -2, 2), # pitch velocity
            constrain(v_local[2], -2, 2)) # yaw velocity

def exponential_ramp(target_value: float = 0, lower_threshold:int = 1000, upper_threshold:int = 2000):
    target_value = min(target_value, upper_threshold)

    num_steps = (target_value / 200) * e

    k = np.log(target_value / lower_threshold) / (num_steps - 1)
    values = lower_threshold * np.exp(k * np.arange(num_steps))

    return np.int32(np.minimum(values, upper_threshold))

def normalize_radians(angle):
    return (angle + 2 * np.pi) % (2 * np.pi)

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def remap(x, min_old, max_old, min_new, max_new):
    return (x - min_old) * (max_new - min_new) / (max_old - min_old) + min_new


# Ensure the log directory exists
log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'log')
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_dir, 'nav_data_fetcher.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class DataFetcher:
    def __init__(self, address='localhost:50051'):
        self.channel = grpc.insecure_channel(address)
        self.stub = api_pb2_grpc.DriverManagerStub(self.channel)
        logging.info(f"DataFetcher initialized with address: {address}")

    def get_imu_data(self):
        try:
            logging.info("Fetching IMU data")
            request = api_pb2.GetRequest(req='')
            if request is None:
                logging.error("Request object is None")
                return None
            response = self.stub.GetImuDataRPC(request)
            logging.info("IMU data fetched successfully")
            return {
                'gyro': (response.gyro.x, response.gyro.y, response.gyro.z),
                'accel': (response.acc.x, response.acc.y, response.acc.z),
            }
        except grpc.RpcError as e:
            logging.error(f"gRPC call failed: {e}")
            return None

    def get_sonar_data(self):
        try:
            logging.info("Fetching Sonar data")
            request = api_pb2.GetRequest(req='')
            if request is None:
                logging.error("Request object is None")
                return None
            response = self.stub.GetSonarDataRPC(request)
            logging.info("Sonar data fetched successfully")
            return {
                'distance': response.sonar
            }
        except grpc.RpcError as e:
            logging.error(f"gRPC call failed: {e}")
            return None

    def get_attitude_data(self):
        try:
            logging.info("Fetching Attitude data")
            request = api_pb2.GetRequest(req='')
            if request is None:
                logging.error("Request object is None")
                return None
            response = self.stub.GetAttitudeDataRPC(request)
            logging.info("Attitude data fetched successfully")
            return {
                'orientation': (response.orient.x, response.orient.y, response.orient.z),
            }
        except grpc.RpcError as e:
            logging.error(f"gRPC call failed: {e}")
            return None

    def get_odometry_data(self):
        try:
            logging.info("Fetching Odometry data")
            request = api_pb2.GetRequest(req='')
            if request is None:
                logging.error("Request object is None")
                return None
            response = self.stub.GetOdometryDataRPC(request)
            logging.info("Odometry data fetched successfully")
            return {
                'position': (response.pos.x, response.pos.y, response.pos.z),
                'velocity': (response.vel.x, response.vel.y, response.vel.z)
            }
        except grpc.RpcError as e:
            logging.error(f"gRPC call failed: {e}")
            return None

    def get_optical_flow_data(self):
        try:
            logging.info("Fetching Optical Flow data")
            request = api_pb2.GetRequest(req='')
            if request is None:
                logging.error("Request object is None")
                return None
            response = self.stub.GetOpticalFlowDataRPC(request)
            logging.info("Optical Flow data fetched successfully")
            return {
                'quality': response.quality,
                'flow_rate_x': response.flow_rate_x,
                'flow_rate_y': response.flow_rate_y,
                'body_rate_x': response.body_rate_x,
                'body_rate_y': response.body_rate_y,
            }
        except grpc.RpcError as e:
            logging.error(f"gRPC call failed: {e}")
            return None

    def get_flags_data(self):
        try:
            logging.info("Fetching Flags data")
            request = api_pb2.GetRequest(req='')
            if request is None:
                logging.error("Request object is None")
                return None
            response = self.stub.GetFlagsDataRPC(request)
            logging.info("Flags data fetched successfully")
            return response
        except grpc.RpcError as e:
            logging.error(f"gRPC call failed: {e}")
            return None