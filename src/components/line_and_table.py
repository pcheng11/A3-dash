from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
import dash_table
from action import get_table_data, get_time_line, name_diff_table_2_timeline
import json
import dash

dataframe = get_table_data()
# def get_table_data() -> dbc.ListGroup:
#     table_card = dbc.ListGroup(
#                                 [
#                                     dbc.ListGroupItem(
#                                         [
#                                             html.Div(
#                                                 [
#                                                     dbc.Row([
#                                                         dbc.Col(
#                                                             data[i]['country'],
#                                                             width=6
#                                                         ),
#                                                         dbc.Col(
#                                                             data[i]['cases'],
#                                                             width=6
#                                                         )
#                                                     ])
#                                                 ]
#                                             )
#                                         ]
#                                     )
#                                     for i in range(0, len(data))
#                                 ]
#                             )
#     return table_card

table = dash_table.DataTable(
        id="country-table",
        data=dataframe.to_dict('records'),
        columns=[
            {"name": "Country", "id": "Country"},
            {
                "name": "Cases",
                "id": "Cases",
                "type": "numeric",
            },
            {
                "name": "Deaths",
                "id": "Deaths",
                "type": "numeric",
            },
        ],
        editable=False,
        row_selectable='single',
        style_as_list_view=True,
        fixed_rows={"headers": True},
        style_table={
            "width": "100%",
            'overflowY': 'scroll',
             'height': '100%'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_header={
            "fontWeight": "bold",
            "font": "Lato, sans-serif",
            "height": "1.5vw",
        },
        style_cell={
            "font-family": "Lato, sans-serif",
            "border-bottom": "0.01rem solid #1C1C1C",
            "backgroundColor": "#000000",
            "color": "#000000",
            'textOverflow': 'ellipsis',
            "height": "2.8vw",
            'maxWidth': '0.1vw'
        },
        style_cell_conditional=[
            {
                "if": {"column_id": "Country"},
                "color": "#FFFFFF",
            },
            {
                "if": {"column_id": "Cases"},
                "color": "#F4B000",
            },
            {
                "if": {"column_id": "Deaths"},
                "color": "#F73F3F",
            },
        ],
    )

line_chart_cases_card = dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            'USA Cases Timeline',
                                            id='cases-title'
                                        ),
                                        html.Div(
                                            dcc.Graph(
                                                id="cases-timeline",
                                                config={"responsive": False},
                                                style={"height": "100%"}
                                            ),
                                            style={"height": "95%"}
                                        ),
                                    ]
                                ),
                                style={"height": "100%"}
                        ),

line_chart_deaths_card = dbc.Card(
                                dbc.CardBody(
                                    [
                                         html.Div(
                                            'USA Deaths Timeline',
                                            id='deaths-title'
                                        ),
                                        html.Div(
                                            dcc.Graph(
                                                id="deaths-timeline",
                                                config={"responsive": False},
                                                style={"height": "100%"}
                                            ),
                                            style={"height": "95%"}
                                        ),
                                    ]
                                ),
                                style={"height": "100%", 'padding': '0px'}
                            )

line_chart_recovered_card = dbc.Card(
                                dbc.CardBody(
                                    [
                                         html.Div(
                                            'USA Recovered Timeline',
                                            id='recovered-title'
                                        ),
                                        html.Div(
                                            dcc.Graph(
                                                id="recovered-timeline",
                                                config={"responsive": True},
                                                style={"height": "100%"}
                                            ),
                                            style={"height": "95%"}
                                        )
                                    ],
                                ),
                                style={"height": "100%"}
                            )

table_card = dbc.Card(
                        dbc.CardBody(
                            table,
                        ),
                        style={"height": "100%", "overflow-y": "scroll"}
                    )


@app.callback(
    [Output('map-location', "children")],
    [Input('country-table', 'selected_rows')]
)
def get_long_lat(selected_rows):
    if selected_rows is not None:
        return [dataframe.loc[int(selected_rows[0]), 'Location']]
    return [[38, -94]]


@app.callback(
    [Output('click-value', "children")],
    [Input('map', "clickData"), Input('country-table', 'selected_rows')]
)
def get_click(clickData, selected_rows):
    country_name = "US"
    selected_rows_country_name = ""
    ctx = dash.callback_context
    click_source = ""
    if ctx.triggered:
        click_source = ctx.triggered[0]['prop_id'].split('.')[0]
        if click_source == "map":
            hover_text = clickData['points'][0]['hovertext']
            country_name = name_diff_table_2_timeline(hover_text)
        else:
            country_name = dataframe.loc[int(selected_rows[0]), 'Country']
            country_name = name_diff_table_2_timeline(country_name)

    return [country_name]

@app.callback(
    [Output('cases-timeline', "figure"),
     Output('cases-title', 'children')], [
         Input('click-value', "children")
     ])
def update_cases_graph(click_value,
                       line_color="#FFBF00",
                       case_type="confirmed"):
    return line_graph(click_value, line_color, case_type)

@app.callback(
    [Output('deaths-timeline', "figure"),
     Output('deaths-title', 'children')], [
         Input('click-value', "children")
     ])
def update_deaths_graph(click_value, line_color="#FA5858", case_type="deaths"):
    return line_graph(click_value, line_color, case_type)

@app.callback([
    Output('recovered-timeline', "figure"),
    Output('recovered-title', 'children')
], [
    Input('click-value', "children")
])
def update_recovered_graph(click_value, line_color="#31B404", case_type="recovered"):
    return line_graph(click_value, line_color, case_type)



def line_graph(click_value, line_color, case_type):
    data = get_time_line(click_value)
    country_name = click_value
    data["date"] = pd.to_datetime(data["date"], infer_datetime_format=False)

    template_total = "%{customdata} total cases on %{x}<extra></extra>"

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data[case_type],
            name="Total Cases",
            line={"color": line_color},
            mode="lines",
            customdata=data[case_type].to_list(),
            hovertemplate=template_total
        )
    )
    fig.update_layout(
        margin={"r": 5, "t": 5, "l": 5, "b": 5},
        template="plotly_dark",
        autosize=True,
        showlegend=False,
        legend_orientation="h",
        paper_bgcolor="black",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis={"linecolor": "rgba(0,0,0,0)"},
        hoverlabel={"font": {"color": "white"}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis={"tickformat": "%m-%d"},
        font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
        yaxis_title="Number of Cases"
    )
    return fig, country_name + " " + case_type + " Timeline"
