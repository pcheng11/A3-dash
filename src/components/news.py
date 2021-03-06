from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
import requests
import json



api_key = '4116a036cba14ecfa27660f53447ed14'
def get_news() -> dbc.ListGroup:
    query = "http://newsapi.org/v2/everything?q=covid-19&apiKey=4116a036cba14ecfa27660f53447ed14"
    response = requests.get(query)
    data = json.loads(response.content)
    articles = data['articles']
    news_card = dbc.ListGroup(
        [
            dbc.ListGroupItem(
                [
                    html.Div(
                        [   
                            dbc.Row([
                                    html.H5(
                                        articles[i]['title'],
                                        style={"color": "white"}
                                    ),
                                    html.P(
                                        articles[i]['description'],
                                        style={"color": "white"}
                                    ),
                                    html.P(
                                        articles[i]['source']['name'] + ', ' + articles[i]['publishedAt'],
                                        style={"color": "white", "font-size": '1.2vh'}
                                    )
                            ])
                            

                        ],
                        className="news-div",
                    )
                ],
                className="news-piece",
                href=articles[i]['url'],
                target="_blank",
            )
            for i in range(0, len(data['articles']))

        ],
        flush=True,
        style={"overflow-y": "scroll", "height": "100%"}
    )
    return news_card