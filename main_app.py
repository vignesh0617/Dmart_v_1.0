from dash import Dash, html, dcc, callback
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from helper_functions.custom_helpers import *
import time
from pages.home_page import layout as home_page
from pages.login_page import layout as login_page
from pages.page_not_found import layout as page_not_found
from pages.about_page import layout as about_page
from components.navbar import navbar


c =0
app = Dash(name = __name__,external_stylesheets=[dbc.themes.COSMO,dbc.icons.BOOTSTRAP])

app.layout = html.Div(children = [
    dcc.Location(id="url1",refresh=False),
    dcc.Location(id="url2",refresh=False),
    #the token is stored in local web browser for authenticating the user
    dcc.Store(id="token", storage_type = "session", data="") , 
    html.Div(id="app_output",className = "app_bg")
    ])

@callback(
    Output("url2","pathname"),
    Output("app_output","children"),
    Output("token","clear_data"),
    Input("url1","pathname"),
    State("token","data"))
def validate_token_and_update_screen(pathname,token):
    global c
    c+=1
    print(f'''----------------------
            Loop number = {c}
            pathname =========== {pathname}
            ---------------------------''')
    try:
        payload = decode_token(token)
        session_not_over = payload['session_end_time'] > int(time.time())
        if session_not_over:
            if(pathname == main_app.environment_details['home_page_link'] or pathname == main_app.environment_details['login_page_link']):
                print("1.1--------------------")
                # return home_page,False
                return main_app.environment_details['home_page_link'],home_page,False
            elif (pathname == main_app.environment_details['about_page_link']):
                # return about_page, False
                return pathname, about_page, False
            elif(pathname == main_app.environment_details['logout_page_link']):
                print("1.2--------------------")
                main_app.connector = ""
                # return login_page,True
                return main_app.environment_details['logout_page_link'],login_page,True
            else:
                print("1.3--------------------")
                # return page_not_found,False
                return pathname,page_not_found,False
        else:
            print("1.4--------------------")
            # return login_page,False
            return main_app.environment_details['login_page_link'],login_page,False
    except Exception as e:
        print("1.5 ---------------------Not a valid Token")
        # return login_page, False
        return main_app.environment_details['login_page_link'],login_page, False


if(__name__ == "__main__"):
    app.run_server(port = 8051, debug = False)