import threading
from threading import Thread

import grpc
import asyncio
import dash
from dash import dcc
from dash import html
import dash_mantine_components as dmc
import dash.dependencies as dd
import dash_bootstrap_components as dbc
import protos.api_pb2 as api_pb2
import protos.api_pb2_grpc as api_pb2_grpc
import time

dash._dash_renderer._set_react_version('18.2.0')
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE, "/assets/custom.css"])

# Define the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Docs", href="/docs")),
        dbc.NavItem(dbc.NavLink("Analyzer", href="/analyzer")),
        dbc.NavItem(dbc.NavLink("Position checker", href="/position")),
    ],
    brand="Applied Robotics Avia API",
    brand_href="/",
    color="dark",
    dark=True,
    links_left=False
)

footer = dbc.Container(
)

# Overall layout
app.layout = dmc.MantineProvider(
    children=[
        html.Div(
            [
                navbar,  # Include the navigation bar
                dash.page_container,
                footer,  # Include the footer
            ]
        ),
    ],
    forceColorScheme='light'
)

if __name__ == '__main__':
    app.run_server(debug=True)