from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from action import get_countrys_data_dash
import dash_bootstrap_components as dbc
from app import app

labels, cases, recovered, deaths = get_countrys_data_dash()


deaths_pie_chart_card = dbc.Card(
        dbc.CardBody([
            html.Div(
                "World Deaths",
                className="title"
            ),
            html.Div(
                dcc.Graph(
                        id="deaths-pie-chart",
                        style={"height": "100%"} 
                    ),
                    style={"height": "95%"}
            )
        ]),
        style={"height": "100%"}
    )
@app.callback(
        Output('deaths-pie-chart', 'figure'),
        [Input('intermediate-value', 'value')]
    )
def death_pie_chart(value):
    return pie_chart(labels, deaths)


cases_pie_chart_card = dbc.Card(
        dbc.CardBody([
            html.Div(
                "World Cases",
                className="title"
            ),
            html.Div(
                dcc.Graph(
                        id="cases-pie-chart",
                        style={"height": "100%"} 
                    ),
                    style={"height": "95%"}
            )
        ]),
        style={"height": "100%"}
    )
@app.callback(
        Output('cases-pie-chart', 'figure'),
        [Input('intermediate-value', 'value')]
    )
def cases_pie_chart(value):
    return pie_chart(labels, cases)


recovered_pie_chart_card = dbc.Card(
        dbc.CardBody([
            html.Div(
                "World Recovered",
                className="title"
            ),
            html.Div(
                dcc.Graph(
                        id="recovered-pie-chart",
                        style={"height": "100%"} 
                    ),
                    style={"height": "95%"}
            )
        ]),
        style={"height": "100%"}
    )
@app.callback(
        Output('recovered-pie-chart', 'figure'),
        [Input('intermediate-value', 'value')]
    )
def recovered_pie_chart(value):
    return pie_chart(labels, recovered)



def pie_chart(labels, data):

    fig = go.Figure(data=[go.Pie(labels=labels, values=data, hole=.2, textinfo='label+percent',
                             insidetextorientation='radial')])
    fig.update_layout(
        template="plotly_dark",
        font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin = dict(t=0, l=0, r=0, b=0)
    )

    return fig