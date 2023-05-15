from dash import html, callback
from dash.dependencies import Output,Input,State
import dash_bootstrap_components as dbc 
# from components.home_page_contents import layout as home_page_contents

layout = html.Div([
    html.Div([
        "Some Random Contents",
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
    ]),
], id="side-filter-tab-container",className="side-filter-tab-container")
