import grpc
import time
import asyncio
from threading import Thread
from concurrent import futures

from driver.msp_controller import MultirotorControl
from driver.msp_transmitter import serialize, UDPTransmitter
from driver.msp_transmitter import TCPTransmitter
from driver.msp_codes import MSPCodes
import protos.api_pb2 as api_pb2
import protos.api_pb2_grpc as api_pb2_grpc
from protos.api_pb2_grpc import add_DriverManagerServicer_to_server


class MSPDriverManagerGRPC(api_pb2_grpc.DriverManagerServicer):
    def __init__(self, address, type):
        self.transmitter = TCPTransmitter(("192.168.2.113", 5760))
        self.msp_controller = MultirotorControl(self.transmitter)
        self.msp_controller.connect()

        self.rc_send = self.rc_get = [1500, 1500, 1000, 1500, 1000, 1000, 1000, 1000]
           
    async def GetImuDataRPC(self, request, context):
        while True:
            self.msp_controller.msp_read_imu_data()
            data = api_pb2.IMUData(
                gyro=api_pb2.Vector3(x=self.msp_controller.SENSOR_DATA["gyroscope"][0],
                                     y=self.msp_controller.SENSOR_DATA["gyroscope"][1],
                                     z=self.msp_controller.SENSOR_DATA["gyroscope"][2]),
                acc=api_pb2.Vector3(x=self.msp_controller.SENSOR_DATA['accelerometer'][0],
                                    y=self.msp_controller.SENSOR_DATA['accelerometer'][1],
                                    z=self.msp_controller.SENSOR_DATA['accelerometer'][2])
            )
            yield data
            time.sleep(0.05)

    async def GetSonarDataRPC(self, request, context):
        while True:
            self.msp_controller.msp_read_sonar_data()
            data = api_pb2.SonarData(
                sonar=self.msp_controller.SENSOR_DATA["sonar"],
            )
            yield data
            time.sleep(0.05)

    async def GetAnalogDataRPC(self, request, context):
        while True:
            self.msp_controller.msp_read_analog_data()
            data = api_pb2.AnalogData(
                voltage=self.msp_controller.ANALOG['voltage'],
                mAhdrawn=self.msp_controller.ANALOG['mAhdrawn'],
                rssi=self.msp_controller.ANALOG['rssi'],
                amperage=self.msp_controller.ANALOG['amperage'],
            )
            yield data
            time.sleep(0.05)

    async def GetAttitudeDataRPC(self, request, context):
        while True:
            self.msp_controller.msp_read_attitude_data()
            data = api_pb2.AttitudeData(
                orient=api_pb2.Vector3(
                    x=self.msp_controller.SENSOR_DATA['kinematics'][0],
                    y=self.msp_controller.SENSOR_DATA['kinematics'][1],
                    z=self.msp_controller.SENSOR_DATA['kinematics'][2],
                ),
            )
            yield data
            time.sleep(0.05)

    async def GetOdometryDataRPC(self, request, context):
        while True:
            self.msp_controller.msp_read_odom_data()
            data = api_pb2.OdometryData(
                pos=api_pb2.Vector3(
                    x=self.msp_controller.SENSOR_DATA['odom']['position'][0],
                    y=self.msp_controller.SENSOR_DATA['odom']['position'][1],
                    z=self.msp_controller.SENSOR_DATA['odom']['position'][2],
                ),
                vel=api_pb2.Vector3(
                    x=self.msp_controller.SENSOR_DATA['odom']['velocity'][0],
                    y=self.msp_controller.SENSOR_DATA['odom']['velocity'][1],
                    z=self.msp_controller.SENSOR_DATA['odom']['velocity'][2],
                ),
                yaw=self.msp_controller.SENSOR_DATA['odom']['yaw'],
            )
            yield data
            time.sleep(0.05)

    async def GetOpticalFlowDataRPC(self, request, context):
        while True:
            self.msp_controller.msp_read_optical_flow_data()
            data = api_pb2.OpticalFlowData(
                quality=self.msp_controller.SENSOR_DATA["optical_flow"][0],
                flow_rate_x=self.msp_controller.SENSOR_DATA["optical_flow"][1],
                flow_rate_y=self.msp_controller.SENSOR_DATA["optical_flow"][2],
                body_rate_x=self.msp_controller.SENSOR_DATA["optical_flow"][3],
                body_rate_y=self.msp_controller.SENSOR_DATA["optical_flow"][4],
            )
            yield data
            time.sleep(0.05)

    async def GetFlagsDataRPC(self, request, context):
        while True:
            self.msp_controller.msp_read_flags_data()
            data = api_pb2.FlagsData(
                activeSensors=self.msp_controller.CONFIG['activeSensors'],
                armingDisableFlags=self.msp_controller.CONFIG['armingDisableFlags'],
                mode=self.msp_controller.CONFIG['mode'],
            )
            yield data
            time.sleep(0.05)

    async def SendRcDataRPC(self, request, context):
        self.rc_send = [
            request.ail,
            request.ele,
            request.thr,
            request.rud,
            request.aux_1,
            request.aux_2,
            request.aux_3,
            request.aux_4,
        ]
        print(self.rc_send)
        # self.msp_controller.msp_send_rc_cmd(self.rc_send)
        response = api_pb2.StatusData(
            status="RC data send"
        )
        return response
    
async def serve():
    msp_driver_manager_gprc = MSPDriverManagerGRPC(("192.168.2.113", 14550), "udp")

    server = grpc.aio.server()
    add_DriverManagerServicer_to_server(msp_driver_manager_gprc, server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)

    await server.start()
    await server.wait_for_termination()
    
    
if __name__ == "__main__":
    asyncio.run(serve())
    