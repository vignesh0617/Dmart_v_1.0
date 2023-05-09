import dash
import dash_bootstrap_components as dbc
from dash import callback, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from connections.MySQL import *
from helper_functions.custom_helpers import * 
import time
from components.navbar import navbar

#attaching this login page to route "/"
# dash.register_page(__name__,path=main_app.environment_details['login_page_link'])

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
                    dbc.Label("Server" , className = "col-form-label"),                  
                ],width=3),
                dbc.Col([
                    dbc.RadioItems(id = "server" ,
                                    options=[
                                      {"label" : "MySQL" , "value" : "MySQL"},
                                      {"label" : "Oracel" , "value" : "Oracle", "disabled" : True},
                                      {"label" : "PostgreSQL" , "value" : "PostgreSQL", "disabled" : True},
                                  ],
                                   inline = True, value="MySQL"
                                  )
                ],width=9)
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
                        dbc.Button(className="bi bi-eye", id = "show_hide_password" ),
                        dbc.FormFeedback("Password can not be empty", type="invalid")
                    ])                    
                ],width = 9)
            ]),
            html.Br(),

            dbc.Row([
                dbc.Col([
                    dbc.Button("Submit", id ="submit_button" ),
                ],className="d-grid")
            ])
        ])
    ],
    className = "col-5 mx-auto position-absolute top-50 start-50 translate-middle transparent white-text"),
])


#this function is used to show and hide password
@callback(
    Output("password","type"),
    Output("show_hide_password","className"),
    Input("show_hide_password","n_clicks")
)
def show_hide_password(n_clicks):
    if n_clicks  is None :
        raise PreventUpdate
    if n_clicks%2 == 1:
        return "text","bi bi-eye-slash"
    return "password","bi bi-eye"

#handles login requests
@callback(
    Output("token","data"),
    Output("refresh","key"),
    Output("message","children"),
    Input("submit_button","n_clicks"),
    State("username","value"),
    State("password","value"),
    State("server","value")
    )
def login_handler(n_clicks,username, password, server):
    if n_clicks is None:
        raise PreventUpdate
    
    if username != "" and password != "" and username is not None and password is not None: 
        main_app.connector, got_connection = get_connection(username = username , password = password)
        if got_connection:
            payload = {
                "username" : username,
                "password" : password,
                "session_end_time" : int(time.time()) + int(main_app.environment_details["session_time_in_secs"])
            }
            token = create_token(payload= payload)

            return token , "True", "Login Successfull"
        else :
            return "" , "False" ,"Wrong username or password"
    else : 
        raise PreventUpdate

@callback(Output("url1","pathname"),Input("refresh","key"))
def go_to_home_page(key):
    if key == "True":
        return main_app.environment_details['home_page_link']
    else:
        raise PreventUpdate

@callback (
    Output("username","invalid"),
    Output("password","invalid"),
    Input("username","value"),
    Input("password","value"),
    Input("submit_button","n_clicks")
    )
def validate_form(username, password, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    username_invalid = (username =="" or username is None)
    password_invalid = (password =="" or password is None)
    return username_invalid,password_invalid

        