import grpc
import protoc.api_pb2 as api_pb2
import protoc.api_pb2_grpc as api_pb2_grpc
import time

def run():
    while True:
        try:
            # Устанавливаем подключение к серверу
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = api_pb2_grpc.DriverManagerStub(channel)
                # Иницииируем запрос к серверу
                request = api_pb2.GetRequest()
                
                # Получаем поток данных от сервера
                sensor_data_stream = stub.GetSensorDataRPC(request)
                
                # Обрабатываем каждый элемент, пришедший в потоке
                for sensor_data in sensor_data_stream:
                    print(f"Received IMU Data: Gyro: ({sensor_data.imu.gyro.x}, "
                          f"{sensor_data.imu.gyro.y}, {sensor_data.imu.gyro.z}), "
                          f"Accel: ({sensor_data.imu.acc.x}, "
                          f"{sensor_data.imu.acc.y}, {sensor_data.imu.acc.z})")
        except grpc.RpcError as e:
            print(f"RPC Error: {e}")
            print("Пытаемся переподключиться...")
            time.sleep(2)  # Ждём немного перед следующей попыткой
        except KeyboardInterrupt:
            print("Клиент завершает работу.")
            break

if __name__ == '__main__':
    run()