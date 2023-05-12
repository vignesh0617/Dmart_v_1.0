from dash import Dash, html, dcc, callback
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from helper_functions.custom_helpers import *
from helper_functions.routing import validate_token_and_update_screen

app = Dash(name = __name__,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])

app.layout = html.Div(children = [
    dcc.Location(id="url1",refresh=False),
    dcc.Location(id="url2",refresh=False),
    #the token is stored in local web browser for authenticating the user
    dcc.Store(id="token", storage_type = "session", data="") , 
    html.Div(id="app_output",className = "app_bg")
    ])


#logic for routing inside the app
@callback(
    Output("url2","pathname"),
    Output("app_output","children"),
    Output("token","clear_data"),
    Input("url1","pathname"),
    State("token","data"))
def routing(pathname,token):
    return validate_token_and_update_screen(pathname=pathname,token=token)

if(__name__ == "__main__"):
    app.run_server(port = 8051, debug = False)