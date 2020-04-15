import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash
from dash.dependencies import Input, Output, State

from components import world_map, news, line_and_table, pie_chart, header_row, news


# Pie Chart Col
cases_pie_chart_col = dbc.Col(
                        pie_chart.cases_pie_chart_card,
                        width=4,
                        style={"height": "100%"}
                    )
deaths_pie_chart_col = dbc.Col(
                        pie_chart.deaths_pie_chart_card,
                        width=4,
                        style={"height": "100%"}
                    )
recovered_pie_chart_col = dbc.Col(
                        pie_chart.recovered_pie_chart_card,
                        width=4,
                        style={"height": "100%"}
                    )

table_col = dbc.Col(
                line_and_table.table_card,
                width=3,
                style={"height": "100%"}
            )

# Line Graph Col
line_chart_cases_col = dbc.Col(
                line_and_table.line_chart_cases_card,
                width=4,
                style={"height": "100%"}
)
line_chart_deaths_col = dbc.Col(
                line_and_table.line_chart_deaths_card,
                width=4,
                style={"height": "100%"}
)
line_chart_recovered_col = dbc.Col(
                line_and_table.line_chart_recovered_card,
                width=4,
                style={"height": "100%"}
)

map_col = dbc.Col(
                world_map.map_section,
                className="middle-col-map-section",
                width=9,
            )
news_col = dbc.Col(
        dbc.Card(
            dbc.CardBody(
                news.get_news(),
                style={"overflow-y": "scroll", "height": "50vh"}
            ),
            style={"overflow-y": "scroll", "height": "100%"}
        ),
        width=3
)

desktop_body = [
    html.Div(
        id="intermediate-value", children="US", style={"display": "none"}
    ), 
    html.Div(
        id="click-value", children="US", style={"display": "none"}
    ), 
    header_row.header_row_card,
    dbc.Row(
        [   
            table_col,
            dbc.Col(
                [
                    dbc.Row(
                        [
                            cases_pie_chart_col,
                            deaths_pie_chart_col,
                            recovered_pie_chart_col
                        ],
                        style={"height": "25vh", "padding": '5px'}
                    ),
                    dbc.Row(
                        [
                            line_chart_cases_col,
                            line_chart_deaths_col,
                            line_chart_recovered_col
                        ],
                        style={"height": "25vh", "padding": '5px'}
                    )
                ],
                width=9,
            ),

        ],
        style={"height": "50vh", "padding": '5px'}
    ),
    dbc.Row(
        [
            news_col,
            map_col,
        ],
        style={"height": "40vh", "padding": '10px'}
    )
]
    

