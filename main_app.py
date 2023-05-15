from dash import html, dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from callback_functions.custom_helpers import *
from callback_functions.routing import *

main_app.app.layout = html.Div(children = [
    dcc.Location(id="url1",refresh=False),
    dcc.Location(id="url2",refresh=False),
    #the token is stored in local web browser for authenticating the user
    dcc.Store(id="token", storage_type = "session", data="") , 
    html.Div(id="app_output")
    ])

if(__name__ == "__main__"):
    main_app.app.run_server(port = 8051, debug = True)