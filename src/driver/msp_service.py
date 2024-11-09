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
        
        self.sensor_data = {}
        self.analog_data = {}
    
    def update_sensor(self):
        self.msp_controller.basic_info()
        self.msp_controller.msp_read_sensor_data()
        self.sensor_data = self.msp_controller.SENSOR_DATA
        print(self.sensor_data)
           
    async def GetSensorDataRPC(self, request, context):
        while True:
            self.update_sensor()
            data = api_pb2.SensorData(
                imu=api_pb2.IMUData(
                    gyro=api_pb2.Vector3(x=self.sensor_data["gyroscope"][0],
                                         y=self.sensor_data["gyroscope"][1],
                                         z=self.sensor_data["gyroscope"][2]),
                    acc=api_pb2.Vector3(x=self.sensor_data['accelerometer'][0],
                                        y=self.sensor_data['accelerometer'][1],
                                        z=self.sensor_data['accelerometer'][2])
                ),
                att=api_pb2.AttitudeData(
                    ang=api_pb2.Vector3(x=self.sensor_data['kinematics'][0],
                                        y=self.sensor_data['kinematics'][1],
                                        z=self.sensor_data['kinematics'][2])
                ),
                odom=api_pb2.OdometryData(
                    pos=api_pb2.Vector3(x=self.sensor_data['odom']['position'][0],
                                        y=self.sensor_data['odom']['position'][1],
                                        z=self.sensor_data['odom']['position'][2]),
                    vel=api_pb2.Vector3(x=self.sensor_data['odom']['velocity'][0],
                                        y=self.sensor_data['odom']['velocity'][1],
                                        z=self.sensor_data['odom']['velocity'][2]),
                    yaw=self.sensor_data['odom']['yaw']
                ),
                analog=api_pb2.AnalogData(
                    voltage=12.5
                )
            )
            yield data
            time.sleep(0.1)
    
    
async def msp_driver_main():
    msp_driver_manager_gprc = MSPDriverManagerGRPC(("192.168.2.113", 14550), "udp")

    server = grpc.aio.server()
    add_DriverManagerServicer_to_server(msp_driver_manager_gprc, server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    await server.start()
    await server.wait_for_termination()
    
    
if __name__ == "__main__":
    asyncio.run(msp_driver_main())
    