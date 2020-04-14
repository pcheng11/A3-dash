from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import config
from action import get_countrys_data_map
import plotly.express as px
from app import app

map_section = dbc.Card(
                dbc.CardBody(
                        dcc.Graph(id="map", style={'height': '100%'})
                ),
                style={'height': '100%'}
            )

@app.callback(
            Output('map', 'figure'),
            [Input('intermediate-value', 'children')])
def map_callback(value):
    token = config.MAPBOX_TOKEN # you will need your own token

    data = get_countrys_data_map()

    
    data["scaled"] = data["cases"] ** 0.77
    fig = px.scatter_mapbox(
        data, 
        lat="lat", 
        lon="long", 
        color='cases',
        hover_name="country", 
        hover_data=["cases", "deaths", "recovered", "country"],
        size="scaled",
        size_max=100,
        zoom=3,
        color_continuous_scale='oranges'
    )
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)
    fig.data[0].update(
        hovertemplate="%{customdata[3]} <br>Cases: %{customdata[0]}<br>Deaths: %{customdata[1]}<br>Recovered: %{customdata[2]}"
    )
    return fig