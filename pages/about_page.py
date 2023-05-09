from dash import html
from components.navbar import navbar

layout = html.Div([
    navbar,
    html.Div("This is the about page")
])