from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import config
from action import get_countrys_data_map, get_country_data, name_diff_timeline_2_table
import plotly.express as px
from app import app
import requests
import json

header_row_card = dbc.Row([
    dbc.Col(html.Div(
        [
            html.H4("World Cases", style={"color": "white"}),
            html.H5(id="world-cases"),
            html.H5(id="world-deaths"),
            html.H5(id="world-recovered")
        ],
        style={
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
        }),
            width=3,
            style={
                "padding": "10px",
                "height": "100%"
            }),
    dbc.Col([
        dbc.Row([
            dbc.Col(html.Div(
                [html.H4(id="country-name")],
                style={
                    "display": "flex",
                    "flex-direction": "column",
                    "align-items": "center",
                }),
                    width=3,
                ),
            dbc.Col(html.Div(
                [
                    html.H5(id="country-cases"),
                    html.H5("Confirmed", className="footnote")
                ],
                style={
                    "display": "flex",
                    "flex-direction": "column",
                    "align-items": "center",
                }),
                    width=3,
                    ),
            dbc.Col(html.Div(
                [
                    html.H5(id="country-deaths"),
                    html.H5("Deaths", className="footnote")
                ],
                style={
                    "display": "flex",
                    "flex-direction": "column",
                    "align-items": "center",
                }),
                    width=3,
                ),
            dbc.Col(
                html.Div(
                    [
                        html.H5(id="country-recovered"),
                        html.H5("Recovered", className="footnote")
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "align-items": "center",
                    }
                ),
                width=3,
                )
        ],
                style={
                    "padding": "10px",
                    "height": "100%"
                })
    ],
            width=9)
],
                          style={
                              "height": "20vh",
                              "padding": '2px'
                          })

@app.callback(
    [
        Output('country-name', 'children'),
        Output('country-cases', 'children'),
        Output('country-deaths', 'children'),
        Output('country-recovered', 'children'),
    ],
    [Input('intermediate-value', 'children'), Input('click-value', 'children')]
)
def update_header_country(children, country):

    data = get_country_data(name_diff_timeline_2_table(country))
    return data['country']['S'] + " Cases", data['cases']['N'] + " (+" + data['todayCases']['N'] + ")", data['deaths']['N'] + " (+" + data['todayDeaths']['N'] + ")", data['recovered']['N']


@app.callback([
    Output('world-cases', 'children'),
    Output('world-deaths', 'children'),
    Output('world-recovered', 'children'),
], [Input('intermediate-value', 'children')])
def update_header_world(children):
    response = requests.get(config.GLOBAL_STAT_URL)
    data = json.loads(response.content)
    confirmed = 'Confirmed ' + str(data['cases']) + ' (+' + str(data['todayCases']) + ')'
    deaths = 'Deaths ' + str(data['deaths']) + ' (+' + str(data['todayDeaths']) + ')'
    recovered = 'Recovered ' + str(data['recovered'])
    return confirmed, deaths, recovered
