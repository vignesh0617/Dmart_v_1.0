from dash import html

layout = html.Div([
    "Main contents 1" ,
    html.Div("inside 1",className="sample"),
    html.Div("inside 2",className="sample"),
    html.Div("inside 3",className="sample"),
],className="main-content")