import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(__name__, path='/position')

layout = dmc.Center(
    html.Div(
        "Пока что тут ничего нет, меня добавят в будущих версиях",
        style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'height': '100vh',
            'textAlign': 'center'
        }
    )
)

# TODO: реализовать страничку для отображения позиции через web интерфейс