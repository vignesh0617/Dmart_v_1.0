from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    # dbc.Button(
    #         className="btn-primary bi bi-arrow-right-circle-fill arrow-position-2 show-filter-button",
    #         id="show-hide-button"),
    # dbc.Popover(
    #         children=["Show Filters"],
    #         id="show-hide-popover",
    #         target="show-hide-button",
    #         body=True,
    #         trigger="hover",
    #     ),
    html.Span(id="refresh_button", className="bi bi-arrow-clockwise refresh_button_position btn-white circle btn-animated"),
    dbc.Popover(
        children=["Refresh-data"],
        id = "refresh_button_popover",
        target="refresh_button",
        body = True,
        trigger = "hover",
        placement="top"
    ),
    "Main contents 2" ,
    html.Div("inside 1",className="sample"),
    html.Div("inside 2",className="sample"),
    html.Div("inside 3",className="sample"),
],id="main-content-container",className="main-content")