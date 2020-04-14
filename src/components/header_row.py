from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import config
from action import get_countrys_data_map
import plotly.express as px
from app import app
import requests
import json

header_row_card = dbc.Row(
                [
                    dbc.Col(
                        html.H1("COVID-19 INSIGHT"),
                        className="title",
                        width=3
                    ),
                    dbc.Col(
                        [
                            dbc.Row([
                                dbc.Col(
                                    html.Div([
                                        html.H2(
                                            id="world_cases"
                                        ),
                                        html.H4(
                                            "Confirmed",
                                            className="footnote"
                                        )
                                    ],
                                    className="header-class"
                                    ),
                                    width=4
                                ),
                                dbc.Col(
                                    html.Div([
                                        html.H2(
                                            id="world_deaths"
                                        ),
                                        html.H4(
                                            "Deaths",
                                            className="footnote"
                                        )
                                    ],
                                    className="header-class"
                                    ),
                                    width=4
                                ),
                                dbc.Col(
                                    html.Div([
                                        html.H2(
                                            id="world_recovered"
                                        ),
                                        html.H4(
                                            "Recovered",
                                            className="footnote"
                                        )
                                    ],
                                    className="header-class"
                                    ),
                                    width=4
                                )
                            ])
                        ]
                    )
                ],
                style={"height": "10vh", "padding": '5px'}
            )

@app.callback(
    [
        Output('world_cases', 'children'),
        Output('world_deaths', 'children'),
        Output('world_recovered', 'children')
    ],
    [Input('intermediate-value', 'children')]
)
def update_header(value):
    response = requests.get("https://corona.lmao.ninja/all")
    global_data = json.loads(response.content)
    return global_data['cases'], global_data['deaths'], global_data['recovered']