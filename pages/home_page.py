from random import sample
from this import d
import dash_bootstrap_components as dbc
import plotly.express as px
from components.navbar import navbar
from dash import callback, dcc, html
from dash.dependencies import Input, Output , State
from dash.exceptions import PreventUpdate
from callback_functions.custom_helpers import *
from components.side_filter_tab import layout as side_filter_tab
from components.home_page_contents import layout as home_page_contents
from callback_functions.home_page_functions import *

layout = html.Div(children=[
    navbar,
    side_filter_tab,
    home_page_contents
],className="main-container")