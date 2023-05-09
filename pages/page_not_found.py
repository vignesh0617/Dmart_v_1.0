from dash import html,dcc, callback
from dash.dependencies import Output,Input,State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from helper_functions.custom_helpers import main_app
from components.navbar import navbar

layout = html.Div([
    navbar,
    "404 Page Not Found",
    html.Br(),
    dbc.Button("Go Back to Home", id="redirect", className="")
    
])

@callback(
    Output('url1',"pathname",allow_duplicate=True),
    Input("redirect","n_clicks"),prevent_initial_call=True
    )
def redirect(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return main_app.environment_details['home_page_link']