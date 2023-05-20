from dash import html
import dash_bootstrap_components as dbc

# def hightlight_active_row(n_clicks,no_of_rows,no_of_cols):
#     if n

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
    # dbc.Spinner([
    html.Div([
        html.Div([
            "List of Figures ========"
        ],className="top-figures",id="top_figures"),
        html.Div(id="top_table",className="top-table")
    ],id="home_page_contents_top",className="home-page-contents-top"),
    html.Div("demo",id="home_page_contents_bottom"),
    # html.Div("demo",id={"type" : "home_page_contents_bottom", "index":1}),
    # ]),
    
],id="main-content-container",className="main-content")