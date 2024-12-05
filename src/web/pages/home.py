import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(__name__, path='/')

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

# TODO: организовать домашнюю веб страницу с описанием каждого дрона и с навигацией по веб интерфейсу