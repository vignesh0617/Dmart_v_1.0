from dash import html, callback, dcc
from dash.dependencies import Output,Input,State
import dash_bootstrap_components as dbc 
from callback_functions.home_page_functions import create_filter_buttons_figures_and_tables
from callback_functions.side_filter_tab_functions import *


layout = html.Div([
        # dbc.Input(id="query",placeholder="Enter your query here"),  # some add on features that can be used later
        # dbc.Button("Fetch Results",id="execute_query"),
        # dbc.Button(
        #     className="circle bi bi-arrow-right-circle-fill arrow-position",
        #     id="show-hide-button"),
        # dbc.Popover(
        #     children=["Show Filters"],
        #     id="show-hide-popover",
        #     target="show-hide-button",
        #     body=True,
        #     trigger="hover",
        # ),
        
        html.Div([
            html.Span(id="show-hide-button",className="bi bi-funnel-fill filter-icon"),
            html.Button("Clear", id = "clear_filter_button", className="btn-theme1"),
            html.Button("Apply", id = "apply_filter_button", className="btn-theme1")
        ],className="filter-header",id = "filter_header"),

        html.Div(id = "filters",className="side-filter-tab-contents"),
], id="side-filter-tab-container",className="side-filter-tab-container")
