import dash
import importlib.resources
from dash import dcc
from dash import html
import dash.dependencies as dd
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html
from flask import render_template_string


dash.register_page(__name__, path="/docs")


layout = html.Div(
    html.A("See in next time")
)