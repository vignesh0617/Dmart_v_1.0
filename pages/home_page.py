from random import sample
from this import d
import dash_bootstrap_components as dbc
import plotly.express as px
from components.navbar import navbar
from dash import callback, dcc, html
from dash.dependencies import Input, Output , State
from dash.exceptions import PreventUpdate
from helper_functions.custom_helpers import *

sample_data = px.data.gapminder()


layout = html.Div(children = [
    navbar,
    dbc.Row([
    dbc.Col([
        html.Label("Filters : ", className="white-text"),
        dcc.Dropdown( id ="continent_filter",
                        options = sample_data['continent'].sort_values().unique(),
                        value = sample_data['continent'].sort_values().unique()[0]),
        html.Br(),
        dcc.Dropdown(id = "year_filter",
                        options = sample_data['year'].sort_values().unique(),
                        value = sample_data['year'].sort_values().unique()[0])
        
    ],width = 3 , className = "border-end"),
    dbc.Col([
        html.H1("Graphs",className="white-text"),
        dbc.Spinner(dcc.Graph(id="graph_output")),
        dbc.Modal([
            dbc.ModalHeader(id = "modal_header"),
            dbc.ModalBody(id = "modal_body"),
            dbc.ModalFooter("Footer"),
        ],id ="main_modal" , is_open = False)
    ],width = 9 )
],className = "margin-0 fill-up-body")
])



@callback(Output("graph_output","figure"),Input("continent_filter","value"),Input("year_filter","value"))
def bar_graph(continent,year):
    if continent is None or year is None :
        raise PreventUpdate
    bar = px.bar(data_frame = sample_data.query("continent == @continent and year == @year"),
          x = 'country',
          y = 'pop',
          title = f"Population in {continent}  Continent in Year : {year}")
    return bar


@callback (
    Output("modal_header","children"),
    Output("modal_body","children"),
    Output("main_modal","is_open"),
    Input("graph_output","clickData"),
    State("continent_filter","value"),
    State("year_filter","value"),
    State("main_modal","is_open"),
    prevent_initial_call =True
    )
def display_modal(clickData,continent,year,is_open):
    main_app.label = clickData['points'][0]['label']
    value = clickData['points'][0]['value']
    main_app.continent_filter = continent
    main_app.year_filter = year
    return f"{main_app.label.title()} - Details Report",[main_app.generate_modal(column,sample_data) for column in sample_data.columns],not is_open



# layout = html.Div([
#     navbar,
#     body
# ])
