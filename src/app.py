import dash
import flask

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

external_stylesheets = [
    dbc.themes.BOOTSTRAP
]

meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
]

app = dash.Dash(__name__, meta_tags=meta_tags, external_stylesheets=external_stylesheets)
app.server.secret_key = 'notterriblysecret'
server = app.server