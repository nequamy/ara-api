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


class DataFetcher:
    def __init__(self, address='localhost:50051'):
        self.channel = grpc.insecure_channel(address)
        self.stub = api_pb2_grpc.DriverManagerStub(self.channel)

    def get_imu_data(self):
        response = self.stub.GetImuDataRPC(api_pb2.GetRequest(req=''))
        for data in response:
            return data

    def get_sonar_data(self):
        response = self.stub.GetSonarDataRPC(api_pb2.GetRequest(req=''))
        for data in response:
            return data

    def get_attitude_data(self):
        response = self.stub.GetAttitudeDataRPC(api_pb2.GetRequest(req=''))

        return {
            'orientation':      (response.orient.x, response.orient.y, response.orient.z),
        }

    def get_odometry_data(self):
        response = self.stub.GetOdometryDataRPC(api_pb2.GetRequest(req=''))

        return {
            'position':         (response.pos.x, response.pos.y, response.pos.z),
            'velocity':         (response.vel.x, response.vel.y, response.vel.z)
        }

    def get_optical_flow_data(self):
        response = self.stub.GetOpticalFlowDataRPC(api_pb2.GetRequest(req=''))
        for data in response:
            return data

    def get_flags_data(self):
        response = self.stub.GetFlagsDataRPC(api_pb2.GetRequest(req=''))
        for data in response:
            return data
