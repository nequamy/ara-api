import threading
from threading import Thread

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
        dcc.Graph(id='gyro-data-graph'),
        dcc.Graph(id='accelerometer-data-graph'),
        dcc.Interval(
            id='interval-component',
            interval=50,
            n_intervals=0
        ),
    ]
)


@app.callback(
    [dd.Output('gyro-data-graph', 'figure'),
     dd.Output('accelerometer-data-graph', 'figure')],
    [dd.Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # Копируем последние 200 данных, если их больше 200
    last_data = sensor_data_list[-200:] if len(sensor_data_list) > 200 else sensor_data_list

    if len(last_data) == 0:
        return {'data': [], 'layout': {'title': 'Нет данных'}}

    # Получаем данные для заполнения графика
    x_values = list(range(len(last_data)))
    gyro_x = [data.imu.gyro.x for data in last_data]
    gyro_y = [data.imu.gyro.y for data in last_data]
    gyro_z = [data.imu.gyro.z for data in last_data]

    acc_x = [data.imu.acc.x for data in last_data]
    acc_y = [data.imu.acc.y for data in last_data]
    acc_z = [data.imu.acc.z for data in last_data]

    # Создаём график
    gyro_figure = {
        'data': [
            {'x': x_values, 'y': gyro_x, 'type': 'line', 'name': 'Гироскоп X'},
            {'x': x_values, 'y': gyro_y, 'type': 'line', 'name': 'Гироскоп Y'},
            {'x': x_values, 'y': gyro_z, 'type': 'line', 'name': 'Гироскоп Z'},
        ],
        'layout': {'title': 'Данные гироскопа'}
    }

    accelerometer_figure = {
        'data': [
            {'x': x_values, 'y': acc_x, 'type': 'line', 'name': 'Акселерометр X'},
            {'x': x_values, 'y': acc_y, 'type': 'line', 'name': 'Акселерометр Y'},
            {'x': x_values, 'y': acc_z, 'type': 'line', 'name': 'Акселерометр Z'},
        ],
        'layout': {
            'title': 'Accelerometer Data',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Value'},
            'showlegend': True
        }
    }

    return gyro_figure, accelerometer_figure


async def grpc_client():
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


def start_grpc_client():
    asyncio.run(grpc_client())

if __name__ == '__main__':
    # Запускаем gRPC клиент в отдельном потоке
    grpc_thread = threading.Thread(target=start_grpc_client, daemon=True)
    grpc_thread.start()

    # Запускаем сервер Dash
    app.run_server(debug=True)