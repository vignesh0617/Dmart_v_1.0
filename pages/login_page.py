import dash_bootstrap_components as dbc
from dash import html
from connections.MySQL import *
from callback_functions.custom_helpers import *
from components.navbar import navbar
from callback_functions.login_page_functions import *

layout= html.Div(children = [
    navbar,
    html.Div(id="refresh",key="False"),
    #building the login page   
    dbc.Card([
        dbc.CardHeader("Login",className = "text-center fw-bold"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label(id="message")
                ],className = "text-center fw-bold")
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Label("Username", className="col-form-label")
                ],width = 3),
                dbc.Col([
                    dbc.Input(id="username",type="text"),
                    dbc.FormFeedback("Username can not be empty", type="invalid")
                ],width = 9)
            ]), 
            html.Br(),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Password", className="col-form-label")
                ],width = 3),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.Input(id="password",type="password"),
                        dbc.Button(className="bi bi-eye", id = "show_hide_password" , style= {"border-radius": "0px 7px 7px 0px"}),
                        dbc.FormFeedback("Password can not be empty", type="invalid")
                    ])                    
                ],width = 9)
            ]),
            html.Br(),

            dbc.Row([
                dbc.Col([
                    dbc.Button("Submit", id ="submit_button"),
                ],className="d-grid")
            ])
        ])
    ],
    className = "col-5 mx-auto position-absolute top-50 start-50 translate-middle transparent white-text"),
],className="app_bg")

        