import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = dbc.Container([

])

# TODO: организовать подсасывание html, который сгенерировал readthedocs на основе папки docs из ветки feature/docs