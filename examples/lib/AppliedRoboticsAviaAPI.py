import asyncio
import grpc
import protos.api_pb2 as api_pb2
from protos.api_pb2_grpc import DriverManagerStub, NavigationManagerStub

# TODO: написать рабочую библиотеку для управления дроном с помощью RPC

class AppliedRoboticsAviaAPI:
    """
    Provides an interface to call RPC services sequentially.
    """

    def __init__(self, nav_address='localhost:50052', driver_address='localhost:50051'):
        """
        Initializes the AppliedRoboticsAviaAPI.
        """
        self.nav_channel = grpc.insecure_channel(nav_address)
        self.driver_channel = grpc.insecure_channel(driver_address)

        self.nav_stub = NavigationManagerStub(self.nav_channel)
        self.driver_stub = DriverManagerStub(self.driver_channel)

    def takeoff(self, altitude):
        """
        Calls the takeoff service from NavigationManagerGRPC
        """
        request = api_pb2.AltitudeSetData(altitude=altitude)
        response = self.nav_stub.TakeOFF(request)
        return response.status

    def land(self):
        """
        Calls the land service from NavigationManagerGRPC
        """
        request = api_pb2.AltitudeSetData(altitude=0)
        response = self.nav_stub.Land(request)
        return response.status

    def move_by_point(self, x, y):
        """
        Calls the move service from NavigationManagerGRPC
        """
        request = api_pb2.PointData(
            point=api_pb2.Vector3(
                x=x,
                y=y,
                z=0, # not available now (TODO)
            )
        )
        response = self.nav_stub.Move(request)
        return response.status


    def set_velocity(self, vx, vy):
        """
        Calls the set_speed service from NavigationManagerGRPC
        """
        request = api_pb2.VelocityData(
            velocity=api_pb2.Vector3(
                x=vx,
                y=vy,
                z=0, # not available now (TODO)
            )
        )
        response = self.nav_stub.SetVelocity(request)
        return response.status

    def get_imu_data(self):
        response = self.driver_stub.GetImuDataRPC(api_pb2.GetRequest(req=''))
        return {
            'gyro':             (response.gyro.x, response.gyro.y, response.gyro.z),
            'accel':            (response.acc.x, response.acc.y, response.acc.z),
        }

    def get_sonar_data(self):
        response = self.driver_stub.GetSonarDataRPC(api_pb2.GetRequest(req=''))
        return {
            'distance':         response.sonar
        }

    def get_attitude_data(self):
        response = self.driver_stub.GetAttitudeDataRPC(api_pb2.GetRequest(req=''))

        return {
            'orientation':      (response.orient.x, response.orient.y, response.orient.z),
        }

    def get_odometry_data(self):
        response = self.driver_stub.GetOdometryDataRPC(api_pb2.GetRequest(req=''))

        return {
            'position':         (response.pos.x, response.pos.y, response.pos.z),
            'velocity':         (response.vel.x, response.vel.y, response.vel.z)
        }

    def get_optical_flow_data(self):
        response = self.driver_stub.GetOpticalFlowDataRPC(api_pb2.GetRequest(req=''))
        return {
            'quality':          response.quality,
            'flow_rate_x':      response.flow_rate_x,
            'flow_rate_y':      response.flow_rate_y,
            'body_rate_x':      response.body_rate_x,
            'body_rate_y':      response.body_rate_y,
        }
