
import jwt
import dash_bootstrap_components as dbc
from dash import html, Dash

#class for creating the reconciliation app
class reconciliation_app:
    def __init__(self):
        self.app = Dash(name = "__main__",external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])
        self.connector = None
        self.cursor = None
        self.table1 = None
        self.environment_details = {}
        self.assign_environment_details()
        
    #used to read the environment.txt file and assign the values to reconciliation_app
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

#for creating JWT
def create_token(payload, 
                secret_key = main_app.environment_details['secret_key'], 
                algorithm = main_app.environment_details['algorithm']):
    return jwt.encode(payload, secret_key, algorithm)

#for decoding JWT
def decode_token(token, 
                secret_key = main_app.environment_details['secret_key'], 
                algorithm = main_app.environment_details['algorithm']):
    return jwt.decode(token, secret_key, algorithm)
    
#For creating a dash table from a dataframe and assign specific callback functions
def create_dash_table_from_data_frame(data_frame,table_id,key_col_number):
    table_headings = []
    table_records = []
    no_of_rows = len(data_frame.index) 
    no_of_cols = len(data_frame.columns)

    for col_label in data_frame.columns:
        table_headings.append(
            html.Th(
                children = col_label.title()
            )
        )
    
    for row in range(no_of_rows):
        records = []
        for col in range(no_of_cols):
            records.append(
                html.Td(
                    children = data_frame.iloc[row,col],
                    # id = f"{table_id}_row{row}_col{col}"
                    id = {
                        'type' : f"{table_id}_rowd_ata",
                        'index' : f"{row}{col}"
                    }
                )
            )
        table_records.append(
            html.Tr(
                children = records,
                id = {
                    'type' : f"{table_id}",
                    'index' : row
                },
                # id = f"{table_id}_row{row}",
                key = data_frame.iloc[row,key_col_number]
            )
        )
    final_table = html.Table([
        html.Thead(
            html.Tr(
                table_headings
            )
        ),
        html.Tbody(
            table_records
        )
    ],id = table_id ,className="table table-hover table-light")

    return final_table