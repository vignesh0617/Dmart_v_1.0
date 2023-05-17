from dash import html, callback
from dash.dependencies import Output,Input,State
import dash_bootstrap_components as dbc 
from callback_functions.home_page_functions import create_filter_buttons



layout = html.Div([
    html.Div([
        # dbc.Input(id="query",placeholder="Enter your query here"),  # some add on features that can be used later
        # dbc.Button("Fetch Results",id="execute_query"),
        dbc.Button(
            className="btn-primary bi bi-arrow-right-circle-fill arrow-position show-filter-button",
            id="show-hide-button"),
        dbc.Popover(
            children=["Show Filters"],
            id="show-hide-popover",
            target="show-hide-button",
            body=True,
            trigger="hover",
        ),
        
        dbc.Label ("Filters : ",className = "main-filter-label" ),
        html.Div([
            html.Div(id = "filters"),
        ],className="side-filter-tab-contents"),
        

    ]),
], id="side-filter-tab-container",className="side-filter-tab-container")
