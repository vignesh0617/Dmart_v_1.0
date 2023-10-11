from dash import html,dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from connections.MySQL import get_data_as_data_frame
from components.data_quality_dashboard import layout as data_quality_dashboard
from components.data_migration_dashboard import layout as data_migration_dashboard

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


    data_quality_dashboard,
    data_migration_dashboard,


    html.Div([dbc.Spinner(color="primary"),html.Br(),"Loading .... Please Wait"],id="loading_screen",className="loading-screen")

],id="main-content-container",className="main-content")