from dash import html,dcc, callback
from dash.dependencies import Output,Input,State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from callback_functions.custom_helpers import main_app
from components.navbar import navbar

layout = html.Div([
    navbar,
    html.Div([
        "404 Page Not Found",
        html.Br(),
        dbc.Button("Go Back to Home", id="redirect", className="")
    ],id="page_not_found_body")
    
    
],id="page_not_found_container")

@callback(
    Output('url1',"pathname",allow_duplicate=True),
    Input("redirect","n_clicks"),prevent_initial_call=True
    )
def redirect(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return main_app.environment_details['home_page_link']