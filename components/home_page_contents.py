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
    html.Span(id="refresh_button", className="bi bi-arrow-clockwise refresh_button_position btn btn-white circle btn-animated"),
    dbc.Popover(
        children=["Refresh-data"],
        id = "refresh_button_popover",
        target="refresh_button",
        body = True,
        trigger = "hover",
        placement="top"
    ),
    html.Div(id="home_page_contents_top"),
    html.Div(id="home_page_contents_bottom")
],id="main-content-container",className="main-content")