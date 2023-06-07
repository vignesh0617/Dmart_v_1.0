from dash import html,dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from connections.MySQL import get_data_as_data_frame
# def hightlight_active_row(n_clicks,no_of_rows,no_of_cols):
#     if n

layout = html.Div([
    html.Span(id="refresh_button", className="bi bi-arrow-clockwise refresh_button_position btn-white circle btn-animated"),
    
    dbc.Popover(
        children=["Refresh-data"],
        id = "refresh_button_popover",
        target="refresh_button",
        body = True,
        trigger = "hover",
        placement="top"
    ),

    # html.Div(id="applied_filter_info",className = "applied_filters"),
    
    html.Div([
            html.Div([
                dcc.Graph(id="fig_1"),
                dcc.Graph(id="fig_2"),
        ],className="top-figures",id="top_figures"), 
        html.Div(id="top_table",className="top-table")
    ],id="home_page_contents_top",className="home-page-contents-top"),
    html.Div([
        html.Div(id="bottom_table",className = "bottom-table"),
        html.Div(id="bottom_table_failed_records",className="bottom-table-failed-records")
    ],id="home_page_contents_bottom",className="home-page-contents-bottom"),

    html.Div([dbc.Spinner(color="primary"),html.Br(),"Loading .... Please Wait"],id="loading_screen",className="loading-screen")

    # html.Div("demo",id={"type" : "home_page_contents_bottom", "index":1}),
    
],id="main-content-container",className="main-content")