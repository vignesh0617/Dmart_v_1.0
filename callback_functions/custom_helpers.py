# import ctypes
import jwt
import dash_bootstrap_components as dbc
from dash import html, Dash
class reconciliation_app:
    def __init__(self):
        self.app = Dash(name = "__main__",external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])
        self.connector = None
        self.cursor = None
        self.year_filter = ""
        self.continent_filter = ""
        self.label = ""
        self.value = ""
        self.environment_details = {}
        self.assign_environment_details()
        
    
    def assign_environment_details(self):
        file = open("environment.txt","r")
        for line in file:
            if(line != "\n" and line.replace(" ","")!=""):
                for[key,value] in [line.rstrip().split(" = ")]:
                    self.environment_details[key] = value
    
    def generate_modal(self,column_name,data):
        layout = dbc.Row([
                    dbc.Col([
                        dbc.Label(column_name.title())
                    ],width = 3),
                    dbc.Col([
                        dbc.Input(value = data.query(f"continent == '{self.continent_filter}' and country == '{self.label}' and year == {self.year_filter}")[column_name], disabled= True)
                    ],width = 6),html.Br(),html.Br()
                ])
        return layout
    def __str__(self) -> str:
        return (f'{self.connector} - {self.environment_details} ')

main_app = reconciliation_app()

def create_token(payload, 
                secret_key = main_app.environment_details['secret_key'], 
                algorithm = main_app.environment_details['algorithm']):
    return jwt.encode(payload, secret_key, algorithm)

def decode_token(token, 
                secret_key = main_app.environment_details['secret_key'], 
                algorithm = main_app.environment_details['algorithm']):
    return jwt.decode(token, secret_key, algorithm)
    

