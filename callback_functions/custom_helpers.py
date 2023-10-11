
import jwt
import dash_bootstrap_components as dbc
from dash import html, Dash
import pandas as pd
#class for creating the reconciliation app
class reconciliation_app:
    def __init__(self):
        self.app = Dash(name = "__main__",external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])
        self.connector = None
        self.cursor = None
        self.environment_details = {}
        self.assign_environment_details()
        
    #used to read the environment.txt file and assign the values to reconciliation_app
    def assign_environment_details(self):
        file = open(file = "environment.txt",mode ="r")
        for line in file:
            if(line != "\n" and line.replace(" ","")!=""):
                for[key,value] in [line.rstrip().split(" = ")]:
                    self.environment_details[key] = value
    
    # Function to generate a modal screen on clicking a data point on bar graph
    # def generate_modal(self,column_name,data):
    #     layout = dbc.Row([
    #                 dbc.Col([
    #                     dbc.Label(column_name.title())
    #                 ],width = 3),
    #                 dbc.Col([
    #                     dbc.Input(value = data.query(f"continent == '{self.continent_filter}' and country == '{self.label}' and year == {self.year_filter}")[column_name], disabled= True)
    #                 ],width = 6),html.Br(),html.Br()
    #             ])
    #     return layout
    # def __str__(self) -> str:
    #     return (f'{self.connector} - {self.environment_details} ')

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
    
# For creating a dash table from a dataframe
# data_frame_original ---> table will be created based on this dataframe
# table_id ---> this table id should be unique for identifying a table
# key_col_number ----> 0th index. each row will store this correspoding data_frame_original.iloc[<row>,key_column_number] in its "key" attribute. This can be used later if required
# action_col_number --->0th index. a link kind of style will be applied to col_number mentioned here. Define a corresponding function to get executed when this data is pressed
# primary_key_col_numbers ----> index's mentioned here, will get saved in form of dicitonary [{"col name1" : "vale1" },{"col name2" : "vale2" }......{{"col namen" : "valen" }}]
# capital_headings ----> Headings of the table header will be Capital letters if this value is True else it will be Title
# col_numbers_to_omit ---->0th index. these index's will be omitted while creating tables in front end  
def create_dash_table_from_data_frame2(
        data_frame_original,
        table_id,
        key_col_number,
        action_col_numbers = [],
        primary_kel_column_numbers = [],
        capital_headings=False,
        col_numbers_to_omit = []
    ):

    # creates a duplicate data_frame which will omit the col_number mentioned in  "col_numbers_to_omit"
    if col_numbers_to_omit: # this if block will execute only if col_numbers_to_omit array is not empty
        col_range = []
        for i in range(data_frame_original.shape[1]):
            if(i not in col_numbers_to_omit):
                col_range.append(i)
        
        data_frame = data_frame_original.iloc[:,col_range]
    else :
        data_frame = data_frame_original

    table_headings = [] # stores all th html values
    table_records = [] # stores all td html vales
    no_of_rows = len(data_frame.index) 
    no_of_cols = len(data_frame.columns)

    
    for col_label in data_frame.columns:
        table_headings.append(
            html.Th(
                children = col_label.upper() if capital_headings else col_label.title()
            )
        )
    
    unique_id = 0 # this unique_id is used to identify each key attribute in "td" 
    for row in range(no_of_rows):
        records = []
        for col in range(no_of_cols):
            records.append(
                html.Td(
                    children = data_frame.iloc[row,col],
                    id = {'type' : f"{table_id}_row_data",'index' : unique_id} if col in action_col_numbers else f"{table_id}_row_data_row-{row}_col-{col}" ,
                    key = {"column_name" : data_frame_original.columns[col],"column_data" : data_frame_original.iloc[row,col] , "primary_keys" : [{data_frame_original.columns[index-1] : data_frame_original.iloc[row,index-1] } for index in primary_kel_column_numbers ]} if col in action_col_numbers else {"column_name" : data_frame_original.columns[col],"column_data" : data_frame_original.iloc[row,col] },
                    className = "table_action" if col in action_col_numbers and data_frame.iloc[row,col]!=0 else ""
                )
            )
            if col in action_col_numbers:
                unique_id+=1
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


#this will read the queries from queries.txt file and return a dictionary as { table_name1 : query1, table_name2 : query2 .... }
def return_sql_queries_from_file():
    file = open(file = "queries.txt",mode = 'r')
    lines = file.readlines()
    queries = {}
    temp_query = ""
    table_name = ""
    for line in lines :
        if len(line.strip()) :
            if line.lower().find("table_name :") != -1 or line.lower().find("view_name :") != -1:
                table_name = line.split(" : ")[1][:-1]
            elif line[-2] != ";":
                temp_query+=line
            elif line[-2] == ";":
                temp_query+=line[:-2]
                queries[table_name] = temp_query
                temp_query = ""
    return queries


# For creating a dash table from a dataframe
# data_frame_original ---> table will be created based on this dataframe
# table_id ---> this table id should be unique for identifying a table
# key_col_number ----> 0th index. each row will store this correspoding data_frame_original.iloc[<row>,key_column_number] in its "key" attribute. This can be used later if required
# action_col_number --->0th index. a link kind of style will be applied to col_number mentioned here. Define a corresponding function to get executed when this data is pressed
# primary_key_col_numbers ----> 1st index . index's mentioned here, will get saved in form of dicitonary [{"col name1" : "vale1" },{"col name2" : "vale2" }......{{"col namen" : "valen" }}]
# capital_headings ----> Headings of the table header will be Capital letters if this value is True else it will be Title
# col_numbers_to_omit ---->0th index. these index's will be omitted while creating tables in front end  
# select_record_type ------> indicates if to select the single(radio button) or multiple(check box) records . Options to pass "single" or "multiple"
# select_record_positon ---> 0th index. where to insert the selected record
def create_dash_table_from_data_frame(
        data_frame_original:pd.DataFrame,
        table_id:str,
        key_col_number:int,
        use_mulitiple_keys:bool = False,
        action_col_numbers:list[int] = [],
        primary_kel_column_numbers:list[int] = [],
        capital_headings:bool =False,
        col_numbers_to_omit:list[int] = [],
        select_record_type:str = "radio",
        select_record_positon:int = None,
        generate_srno:bool = False,
        disable_check_box:bool = True,
        no_records_msg:str = "No Records to display",
    ):
    
    # creates a duplicate data_frame which will omit the col_number mentioned in  "col_numbers_to_omit"
    if col_numbers_to_omit: # this if block will execute only if col_numbers_to_omit array is not empty
        col_range = []
        for i in range(data_frame_original.shape[1]):
            if(i not in col_numbers_to_omit):
                col_range.append(i)
        
        data_frame = data_frame_original.iloc[:,col_range]
    else :
        data_frame = data_frame_original

    
    table_headings = [] # stores all th html values
    table_records = [] # stores all td html vales
    no_of_rows = len(data_frame.index) 
    no_of_cols = len(data_frame.columns)

    for col_label in data_frame.columns:
    
        table_headings.append(
            html.Th(
                children = col_label.upper() if capital_headings else col_label.title()
            )
        )

    if generate_srno:
        table_headings.insert(0,
            html.Th(
                children = "S.NO" if capital_headings else "S.no"
            )
        )

    if select_record_positon is not None :#and (select_record_positon == index ):
        if select_record_type.lower() == 'radio':
            table_headings.insert(select_record_positon,
                html.Th(
                    children = "SELECT" if capital_headings else "Select"
                )
            )
        else : #select_record_type.lower() == 'checkbox' :
            # cb = dbc.Checkbox(id=f"cb_all_{table_id}",label=""),
            table_headings.insert(select_record_positon,
                html.Th(
                    children = [
                        # "Select all",
                        dbc.Checkbox(id=f"cb_all_{table_id}",label="SELECT ALL" if capital_headings else "Select All",disabled= (no_of_rows == 0))
                    ]
                )
            )
    
    unique_id = 0 # this unique_id is used to identify each key attribute in "td" 
    for row in range(no_of_rows):
        records = []
        for col in range(no_of_cols):
            records.append(
                html.Td(
                    children = data_frame.iloc[row,col],
                    id = {'type' : f"{table_id}_row_data",'index' : unique_id} if col in action_col_numbers else {"type":f"{table_id}_row{row}" ,"index" : col},#f"{table_id}_row_data_row-{row}_col-{col}" ,
                    key = {"column_name" : data_frame_original.columns[col],"column_data" : data_frame_original.iloc[row,col] , "primary_keys" : [{data_frame_original.columns[index-1] : data_frame_original.iloc[row,index-1] } for index in primary_kel_column_numbers ]} if col in action_col_numbers else {"column_name" : data_frame_original.columns[col],"column_data" : data_frame_original.iloc[row,col] },
                    className = "table_action" if col in action_col_numbers and data_frame.iloc[row,col]!=0 else ""
                )
            )

                       
            if col in action_col_numbers:
                unique_id+=1
        if generate_srno :
            records.insert(0,
                html.Td(
                    children = row+1,
                    )
            )
        if select_record_positon is not None:#  and select_record_positon == col:
                if select_record_type.lower() == 'radio':
                    records.insert(select_record_positon,
                        html.Td(
                            children = [
                                dbc.RadioButton(id={"type":f"rb_{table_id}","index":row},
                                                label="",
                                                name=[{data_frame_original.columns[index-1] : data_frame_original.iloc[row,index-1] } for index in primary_kel_column_numbers ],
                                                value=False)#=data_frame.iloc[row,key_col_number])
                            ],
                            
                        )
                    )
                else :
                    records.insert(select_record_positon,
                        html.Td(
                            children = [
                                dbc.Checkbox(id={"type":f"cb_{table_id}","index":row},
                                             label="",
                                             name=[{data_frame_original.columns[index-1] : data_frame_original.iloc[row,index-1] } for index in primary_kel_column_numbers ],
                                             disabled=disable_check_box,
                                             value=False)#=data_frame.iloc[row,key_col_number])
                            ],
                            
                        )
                    )
        if use_mulitiple_keys : 
            key_value = dict(data_frame_original.iloc[row,[num-1 for num in primary_kel_column_numbers]])
        else:
            key_value = data_frame_original.iloc[row,key_col_number] 
        table_records.append(
            html.Tr(
                children = records,
                id = {
                    'type' : f"{table_id}_row_number",
                    'index' : row
                },
                # id = f"{table_id}_row{row}",
                key = key_value
            )
        )
    
    if no_of_rows == 0:
        table_records.append(
            html.Tr(
                children = [
                    html.Td(
                        children=no_records_msg,
                        colSpan= len(table_headings),
                        style={'text-align':'center'}
                    )
                ]
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
