from dash import html
from components.navbar import navbar

layout = html.Div([
    navbar,
    html.Div(className="box",
             children=[
                 html.Div(className="fixed",children=["Fixes"]),
                 html.Div(className="remaining",children=["Remaining"]), 
             ])
])