import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.express as px
from dash_iconify import DashIconify
from docutils.nodes import figure

dash.register_page(__name__, path='/analyzer')

fig = px.scatter(width=1000, height=500)

# TODO: реализовать функционал базового анализатора на основе кода из app.py
imu_tabs = dmc.Container(
    children=[
        dmc.Container(children=[dcc.Graph(id='gyro-data-graph', figure=fig)]),
        dmc.Container(children=[dcc.Graph(id='accelerometer-data-graph', figure=fig)]),
        dcc.Interval(
            id='interval-component',
            interval=50,
            n_intervals=0
        ),
    ]
)

motor_tabs = dmc.Container(
    children=[
        dcc.Graph(id='-motor-graph'),
        dcc.Interval(
            id='interval-component',
            interval=50,
            n_intervals=0
        ),
    ]
)

blackbox_tabs = dmc.Container(
    children=[
        dcc.Graph(id='-blackbox-graph'),
        dcc.Interval(
            id='interval-component',
            interval=50,
            n_intervals=0
        ),
    ]
)

layout = html.Div(
    [
        dmc.Tabs(
            [
                dmc.TabsList([
                    dmc.TabsTab(children="IMU",
                                leftSection=DashIconify(icon="ph:drone-duotone", width=30),
                                value="imu"),
                    dmc.TabsTab(children="Motors",
                                leftSection=DashIconify(icon="mdi:motor", width=30),
                                value="motor"),
                    dmc.TabsTab(children="Blackbox",
                                leftSection=DashIconify(icon="mdi:micro-sd", width=30),
                                value="blackbox"),
                ]),
                dmc.TabsPanel(imu_tabs, value="imu"),
                dmc.TabsPanel(motor_tabs, value="motor"),
                dmc.TabsPanel(blackbox_tabs, value="blackbox"),
            ],
            orientation="vertical",
            variant="pills",
            radius="md",

        ),
    ]
)


# @app.callback(
#     [dd.Output('gyro-data-graph', 'figure'),
#      dd.Output('accelerometer-data-graph', 'figure')],
#     [dd.Input('interval-component', 'n_intervals')]
# )
# def update_graph(n):
#     # Копируем последние 200 данных, если их больше 200
#     last_data = imu_data_list[-200:] if len(imu_data_list) > 200 else imu_data_list
#
#     if len(last_data) == 0:
#         return {'data': [], 'layout': {'title': 'Нет данных'}}
#
#     # Получаем данные для заполнения графика
#     x_values = list(range(len(last_data)))
#     gyro_x = [data.imu.gyro.x for data in last_data]
#     gyro_y = [data.imu.gyro.y for data in last_data]
#     gyro_z = [data.imu.gyro.z for data in last_data]
#
#     acc_x = [data.imu.acc.x for data in last_data]
#     acc_y = [data.imu.acc.y for data in last_data]
#     acc_z = [data.imu.acc.z for data in last_data]
#
#     # Создаём график
#     gyro_figure = {
#         'data': [
#             {'x': x_values, 'y': gyro_x, 'type': 'line', 'name': 'Гироскоп X'},
#             {'x': x_values, 'y': gyro_y, 'type': 'line', 'name': 'Гироскоп Y'},
#             {'x': x_values, 'y': gyro_z, 'type': 'line', 'name': 'Гироскоп Z'},
#         ],
#         'layout': {'title': 'Данные гироскопа'}
#     }
#
#     accelerometer_figure = {
#         'data': [
#             {'x': x_values, 'y': acc_x, 'type': 'line', 'name': 'Акселерометр X'},
#             {'x': x_values, 'y': acc_y, 'type': 'line', 'name': 'Акселерометр Y'},
#             {'x': x_values, 'y': acc_z, 'type': 'line', 'name': 'Акселерометр Z'},
#         ],
#         'layout': {
#             'title': 'Accelerometer Data',
#             'xaxis': {'title': 'Time'},
#             'yaxis': {'title': 'Value'},
#             'showlegend': True
#         }
#     }
#
#     return gyro_figure, accelerometer_figure