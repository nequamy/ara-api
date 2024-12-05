import grpc
import asyncio
import dash
from dash import dcc
from dash import html
import dash.dependencies as dd
import dash_bootstrap_components as dbc
import protos.api_pb2 as api_pb2
import protos.api_pb2_grpc as api_pb2_grpc
import time

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Изменяемая переменная для хранения данных сенсоров
sensor_data_list = []

app.layout = html.Div(
    [
        dcc.Graph(id='sensor-data-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1000,  # обновление каждые 1 секунду, можно настроить
            n_intervals=0
        ),
    ]
)

@app.callback(
    dd.Output('sensor-data-graph', 'figure'),
    [dd.Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    if len(sensor_data_list) == 0:
        return {'data': [], 'layout': {'title': 'Нет данных'}}
    
    # Получаем последние данные для заполнения графика
    x_values = list(range(len(sensor_data_list)))
    gyro_x = [data.imu.gyro.x for data in sensor_data_list]
    gyro_y = [data.imu.gyro.y for data in sensor_data_list]
    gyro_z = [data.imu.gyro.z for data in sensor_data_list]

    figure = {
        'data': [
            {'x': x_values, 'y': gyro_x, 'type': 'line', 'name': 'Гироскоп X'},
            {'x': x_values, 'y': gyro_y, 'type': 'line', 'name': 'Гироскоп Y'},
            {'x': x_values, 'y': gyro_z, 'type': 'line', 'name': 'Гироскоп Z'},
        ],
        'layout': {
            'title': 'Данные гиро-датчиков',
            'xaxis': {'title': 'Количество полученных данных'},
            'yaxis': {'title': 'Значение'},
        }
    }
    return figure

async def grpc_client():
    while True:
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
                    sensor_data_list.append(sensor_data)
                    
                    # Ограничиваем длину списка, если нужно
                    if len(sensor_data_list) > 100:  # например, храним только последние 100 данных
                        sensor_data_list.pop(0)
        except grpc.RpcError as e:
            print(f"RPC Error: {e}")
            print("Пытаемся переподключиться...")
            await asyncio.sleep(2)  # Ждем немного перед следующей попыткой
        except KeyboardInterrupt:
            print("Клиент завершает работу.")
            break

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(grpc_client())
    app.run_server(debug=True)