import grpc
import asyncio
import protos.api_pb2 as api_pb2
import protos.api_pb2_grpc as api_pb2_grpc

class APPManagerGRPCClient(object):
    def __init__(self):
        self.imu_data_list = []
        self.sonar_data_list = []
        self.analog_data_list = []
        self.attitude_data_list = []
        self.odometry_data_list = []
        self.optical_flow_data_list = []

    async def get_imu_data_grpc(self):
        try:
            async with grpc.aio.insecure_channel('localhost:50051') as channel:
                stub = api_pb2_grpc.DriverManagerStub(channel)
                request = api_pb2.GetRequest()

                async for imu_data in stub.GetImuDataRPC(request):
                    print(f"Received IMU Data: Gyro: ({imu_data.imu.gyro.x}, "
                          f"{imu_data.imu.gyro.y}, {imu_data.imu.gyro.z}), "
                          f"Accel: ({imu_data.imu.acc.x}, "
                          f"{imu_data.imu.acc.y}, {imu_data.imu.acc.z})")

                    self.imu_data_list.append(imu_data)

                    if len(self.imu_data_list) > 100:
                        self.imu_data_list.pop(0)

                sensor_stream = stub.GetImuDataRPC(request)
                while True:
                    response = await sensor_stream.read()
                    if response == grpc.aio.EOF:
                        break
                    print(
                        "Greeter client received from direct read: " + response.message
                    )
        except grpc.RpcError as e:
            print(f"Imu RPC Error: {e}")
            print("Try to reconnect...")
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            print("Client stopped.")

    async def get_sonar_data_grpc(self):
        try:
            async with grpc.aio.insecure_channel('localhost:50051') as channel:
                stub = api_pb2_grpc.DriverManagerStub(channel)
                request = api_pb2.GetRequest()

                async for sonar_data in stub.GetSonarDataRPC(request):
                    print(f"Received Sensor Data: Sonar: ({sonar_data.sonar}, )")

                    self.sonar_data_list.append(sonar_data)

                    if len(self.sonar_data_list) > 100:
                        self.sonar_data_list.pop(0)

                sonar_stream = stub.GetImuDataRPC(request)
                while True:
                    response = await sonar_stream.read()
                    if response == grpc.aio.EOF:
                        break
                    print(
                        "Greeter client received from direct read: " + response.message
                    )
        except grpc.RpcError as e:
            print(f"Sonar RPC Error: {e}")
            print("Try to reconnect...")
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            print("Client stopped.")

    async def get_analog_data_grpc(self):
        try:
            async with grpc.aio.insecure_channel('localhost:50051') as channel:
                stub = api_pb2_grpc.DriverManagerStub(channel)
                request = api_pb2.GetRequest()

                async for analog_data in stub.GetAnalogDataRPC(request):
                    print(f"Received Analog Data: Voltage: ({analog_data.voltage}),"
                          f"mAhdrawn: ({analog_data.mAhdrawn})"
                          f"rssi: ({analog_data.rssi})"
                          f"amperage: ({analog_data.amperage})")

                    self.analog_data_list.append(analog_data)

                    if len(self.analog_data_list) > 100:
                        self.analog_data_list.pop(0)

                analog_stream = stub.GetAttitudeDataRPC(request)
                while True:
                    response = await analog_stream.read()
                    if response == grpc.aio.EOF:
                        break
                    print(
                        "Greeter client received from direct read: " + response.message
                    )
        except grpc.RpcError as e:
            print(f"AnalogRPC Error: {e}")
            print("Try to reconnect...")
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            print("Client stopped.")

    async def get_attitude_data_grpc(self):
        try:
            async with grpc.aio.insecure_channel('localhost:50051') as channel:
                stub = api_pb2_grpc.DriverManagerStub(channel)
                request = api_pb2.GetRequest()

                async for attitude_data in stub.GetAttitudeDataRPC(request):
                    print(f"Received Sensor Data: Gyro: ({attitude_data.sonar}, )")

                    self.attitude_data_list.append(attitude_data)

                    if len(self.attitude_data_list) > 100:
                        self.attitude_data_list.pop(0)

                attitude_stream = stub.GetAttitudeDataRPC(request)
                while True:
                    response = await attitude_stream.read()
                    if response == grpc.aio.EOF:
                        break
                    print(
                        "Greeter client received from direct read: " + response.message
                    )
        except grpc.RpcError as e:
            print(f"RPC Error: {e}")
            print("Try to reconnect...")
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            print("Client stopped.")

    async def get_sonar_data_grpc(self):
        try:
            async with grpc.aio.insecure_channel('localhost:50051') as channel:
                stub = api_pb2_grpc.DriverManagerStub(channel)
                request = api_pb2.GetRequest()

                async for sonar_data in stub.GetSonarDataRPC(request):
                    print(f"Received Sensor Data: Gyro: ({sonar_data.sonar}, )")

                    self.sonar_data_list.append(sonar_data)

                    if len(self.sonar_data_list) > 100:
                        self.sonar_data_list.pop(0)

                sonar_stream = stub.GetImuDataRPC(request)
                while True:
                    response = await sonar_stream.read()
                    if response == grpc.aio.EOF:
                        break
                    print(
                        "Greeter client received from direct read: " + response.message
                    )
        except grpc.RpcError as e:
            print(f"RPC Error: {e}")
            print("Try to reconnect...")
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            print("Client stopped.")

    async def get_sonar_data_grpc(self):
        try:
            async with grpc.aio.insecure_channel('localhost:50051') as channel:
                stub = api_pb2_grpc.DriverManagerStub(channel)
                request = api_pb2.GetRequest()

                async for sonar_data in stub.GetSonarDataRPC(request):
                    print(f"Received Sensor Data: Gyro: ({sonar_data.sonar}, )")

                    self.sonar_data_list.append(sonar_data)

                    if len(self.sonar_data_list) > 100:
                        self.sonar_data_list.pop(0)

                sonar_stream = stub.GetImuDataRPC(request)
                while True:
                    response = await sonar_stream.read()
                    if response == grpc.aio.EOF:
                        break
                    print(
                        "Greeter client received from direct read: " + response.message
                    )
        except grpc.RpcError as e:
            print(f"RPC Error: {e}")
            print("Try to reconnect...")
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            print("Client stopped.")

    async def get_sonar_data_grpc(self):
        try:
            async with grpc.aio.insecure_channel('localhost:50051') as channel:
                stub = api_pb2_grpc.DriverManagerStub(channel)
                request = api_pb2.GetRequest()

                async for sonar_data in stub.GetSonarDataRPC(request):
                    print(f"Received Sensor Data: Gyro: ({sonar_data.sonar}, )")

                    self.sonar_data_list.append(sonar_data)

                    if len(self.sonar_data_list) > 100:
                        self.sonar_data_list.pop(0)

                sonar_stream = stub.GetImuDataRPC(request)
                while True:
                    response = await sonar_stream.read()
                    if response == grpc.aio.EOF:
                        break
                    print(
                        "Greeter client received from direct read: " + response.message
                    )
        except grpc.RpcError as e:
            print(f"RPC Error: {e}")
            print("Try to reconnect...")
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            print("Client stopped.")



    def start_grpc_client(self):
        asyncio.run(self.get_imu_data_grpc())