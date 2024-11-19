import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from web.pages.analyzer import layout

dash.register_page(__name__, path='/position')

layout = html.Div("next time")


# TODO: реализовать страничку для отображения позиции через web интерфейс