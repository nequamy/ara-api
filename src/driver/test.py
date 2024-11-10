# from concurrent import futures
# import time
# import grpc
# import protos.api_pb2 as api_pb2
# import protos.api_pb2_grpc as api_pb2_grpc

# class DriverManagerServicer(api_pb2_grpc.DriverManagerServicer):
#     def GetSensorDataRPC(self, request, context):
#         # Генерируем поток данных датчиков
#         for _ in range(10):  # Предположим, мы отправляем 10 сообщений
#             sensor_data = api_pb2.SensorData(
#                 imu=api_pb2.IMUData(
#                     gyro=api_pb2.Vector3(x=0.1, y=0.2, z=0.3),
#                     acc=api_pb2.Vector3(x=0.01, y=0.02, z=0.03)
#                 ),
#                 att=api_pb2.AttitudeData(
#                     ang=api_pb2.Vector3(x=0.0, y=1.0, z=1.0)
#                 ),
#                 odom=api_pb2.OdometryData(
#                     pos=api_pb2.Vector3(x=1.0, y=2.0, z=3.0),
#                     vel=api_pb2.Vector3(x=0.0, y=1.0, z=1.0),
#                     yaw=0.5
#                 ),
#                 analog=api_pb2.AnalogData(
#                     voltage=12.5
#                 )
#             )
#             yield sensor_data
#             time.sleep(0.1)  # Задержка для имитации данных в реальном времени

# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     api_pb2_grpc.add_DriverManagerServicer_to_server(DriverManagerServicer(), server)
#     server.add_insecure_port('[::]:50051')
#     server.start()
#     server.wait_for_termination()

# if __name__ == '__main__':
#     serve()

class B():
    def tmp(self):
        print("I am class B")
        
class C():
    def tmp(self):
        print("I am class C")

class A():
    def __init__(self):
        self.b = B()
        self.c = C()
    
    def serialize(self, type):
        match type:
            case "B":
                return B()
            case "C":
                return C()
            
a = A.serialize(A, "C")
a.tmp()