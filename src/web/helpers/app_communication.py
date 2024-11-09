import grpc
import asyncio
import protos.api_pb2 as api_pb2
import protos.api_pb2_grpc as api_pb2_grpc

class APPManagerGRPCClient(object):
    def __init__(self):
        self.sensor_data_list = []

    async def get_sensor_data_grpc(self):
        try:
            # Устанавливаем подключение к серверу
            async with grpc.aio.insecure_channel('localhost:50051') as channel:
                stub = api_pb2_grpc.DriverManagerStub(channel)
                request = api_pb2.GetRequest()

                # Получаем поток данных от сервера
                async for sensor_data in stub.GetSensorDataRPC(request):
                    print(f"Received IMU Data: Gyro: ({sensor_data.imu.gyro.x}, "
                          f"{sensor_data.imu.gyro.y}, {sensor_data.imu.gyro.z}), "
                          f"Accel: ({sensor_data.imu.acc.x}, "
                          f"{sensor_data.imu.acc.y}, {sensor_data.imu.acc.z})")

                    # Добавляем данные в список
                    self.sensor_data_list.append(sensor_data)

                    # Ограничиваем длину списка, если нужно
                    if len(self.sensor_data_list) > 100:  # например, храним только последние 100 данных
                        self.sensor_data_list.pop(0)

                sensor_stream = stub.GetSensorDataRPC(request)
                while True:
                    response = await sensor_stream.read()
                    if response == grpc.aio.EOF:
                        break
                    print(
                        "Greeter client received from direct read: " + response.message
                    )
        except grpc.RpcError as e:
            print(f"RPC Error: {e}")
            print("Пытаемся переподключиться...")
            await asyncio.sleep(2)  # Ждем немного перед следующей попыткой
        except KeyboardInterrupt:
            print("Клиент завершает работу.")

    def start_grpc_client(self):
        asyncio.run(self.get_sensor_data_grpc())