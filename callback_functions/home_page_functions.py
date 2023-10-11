from dash.dependencies import Output, Input, State, ALL
from callback_functions.custom_helpers import main_app
from dash.exceptions import PreventUpdate
from connections.MySQL import *
import dash_bootstrap_components as dbc
from dash import dash_table, html, ctx,dcc , no_update
from numpy import insert
from callback_functions.custom_helpers import create_dash_table_from_data_frame
import plotly.express as px
import pandas as pd
from mysql.connector import errorcode, Error


# Below function was created to toggle filter screen. Uncomment it if requried

# @main_app.app.callback(
#     Output("side-filter-tab-container","style"),
#     Output("main-content-container","style"),
#     Output("clear_filter_button","style"),
#     Output("apply_filter_button","style"),
#     Output("filters","style"),
#     Output("show-hide-button","style"),
#     Input("show-hide-button","n_clicks"),
#     prevent_initial_call=True)
# def show_hide_filter_section(n_clicks):
#     if(n_clicks%2==1):
#         return {"flex-basis":"20%"},{"flex-basis":"80%"},{"opacity":"1"},{"opacity":"1"},{"opacity":"1"},{"color":"green"}
#     else:
#         return {},{},{},{},{},{}


# below function is a additional functionality to query the backend tables directly. Uncomment it to add the feature
# @main_app.app.callback(
#     Output("main-content-container","children"),
#     Input("execute_query","n_clicks"),
#     State("query","value")
# )
# def get_table_data(n_clicks,sql_query):
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         df = get_data_as_data_frame(sql_query=sql_query, cursor= main_app.cursor)
#         return dash_table.DataTable(data=df.to_dict('records'),columns=[{"name" : i, "id" : i} for i in df.columns])


# This function create graphs and filter buttons when the user log's in. And its also triggered when the refresh button is pressed 
@main_app.app.callback(
        Output("filters","children"),
        Output("top_table","children"),
        Output("fig_1", "figure"),
        Output("data_migration_bottom_table","children"),
        Output("fig_3", "figure"),
        Output("fig_4", "figure"),
        Output("fig_5", "figure"),
        Output("fig_6", "figure"),
        Input("refresh_button","n_clicks"),
        State("filter_type","value")
)
def create_filter_buttons_figures_and_tables_and_refresh_data(n_clicks,filter_type_value):

    # gets all the required inputs from the environment.txt file
    # all the values are converted to an array format and stored in corresponding variables
    filter_tables = main_app.environment_details['filter_table_names'].split(',')
    filter_tables_columns = main_app.environment_details['filter_table_columns'].split(',')
    filter_tables_labels = main_app.environment_details['filter_table_labels'].split(',')
    filter_ids = main_app.environment_details['filter_ids'].split(',')
    filter_types = main_app.environment_details['filter_types'].split(',')

    filters = []

    for i in range(len(filter_tables)):
        table_name = filter_tables[i]
        column_name = filter_tables_columns[i]
        column_label = filter_tables_labels[i]
        filter_id = filter_ids[i]
        filter_type = filter_types[i]
        
        sql_1 = f"select distinct {column_name} from {table_name}"
        data_frame = get_data_as_data_frame(sql_query=sql_1  , cursor= main_app.cursor)
        # this was a old layout model for filter buttons
        # layout = html.Div([
        #     dbc.Label(column_label,className = "filter-label"),
        #     dcc.Dropdown(id = filter_id , 
        #                options=data_frame[data_frame.columns[0]],
        #                className = "filter-dropdown",
        #                multi= True,
        #                placeholder= f"Select {column_label} ... ")
        # ],className = "filter-card")

        # this is the new layout model for the filter buttons with select all check box features
        layout = html.Div([
                    dbc.Label(column_label,className = "filter-label"),
                    dbc.DropdownMenu([
                        dbc.Checkbox(id=filter_id+"_select_all",label="Select All"),
                        dbc.Checklist(id=filter_id,
                                      options=data_frame[data_frame.columns[0]],
                                      value=data_frame[data_frame.columns[0]])
                    ],
                    label = "All",
                    id=filter_id+"_drop_down",
                    disabled = False if filter_type == "common" or filter_type == filter_type_value else True,
                    )
                ],className = "filter-card",
                  id = f"filter_card_{i}",
                  style = {} if filter_type == "common" or filter_type == filter_type_value else {"display":"none"} )
        
        filters.append(layout)

    sql_2 = main_app.environment_details["top_table_query"]
    
    data_frame = get_data_as_data_frame(sql_query=sql_2,cursor=main_app.cursor)

    top_table = create_dash_table_from_data_frame(
                    data_frame_original=data_frame, 
                    table_id = main_app.environment_details["top_table_id"] , 
                    key_col_number= int(main_app.environment_details["top_table_key_col_number"])
            )
    
    pie_data_query = '''
    select "No.Of Rules Passed" as "Description", count(*) as "Count" from ( SELECT distinct `Rule Name`, `In_Scope`,`Success`, `Defects` FROM technical_reconciliation where `Defects` = 0) temp union all
    select "No.Of Rules Failed" as "Description", count(*) as "Count" from ( SELECT distinct `Rule Name`, `In_Scope`,`Success`, `Defects` FROM technical_reconciliation where `Defects` != 0) temp 
    '''

    pie_data = get_data_as_data_frame(sql_query=pie_data_query,cursor=main_app.cursor)
    
    pie_chart = px.pie(data_frame = pie_data,
                names = 'Description',
                height=244,
                width=344,
                values = 'Count',
                color='Description',
                title = f"Total Rules = {pie_data.sum()['Count']}<br>No.of Rules Passed Vs No.of Rules Failed",
                color_discrete_map={"No.Of Rules Failed":"red","No.Of Rules Passed":"lime"})

    pie_chart.update_traces(sort=False) 

    pie_chart.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-1,
    xanchor="right",
    x=1
    ))
    


    sql_query = f"select * from DM_Summary"

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    dm_summary_table = create_dash_table_from_data_frame(
        data_frame_original=data_frame,
        table_id="data_migration_bottom_table_contents",
        key_col_number=1,
        # primary_kel_column_numbers=list(map(int,main_app.environment_details["bottom_table_primary_key_column_number"].split(","))),
        # action_col_numbers=[11],
        # col_numbers_to_omit=[12]
        )

    pie_data1 = pd.DataFrame(columns=['Type','Count'],index=['1','2'],data=[['Success',2389],['Failure',455]])
    
    pie_chart1 = px.pie(data_frame=pie_data1,
                   values = pie_data1.columns[1],
                   names = pie_data1.columns[0],
                   title = 'Success vs Failure',
                   color_discrete_sequence = ['#61876E','#FB2576'],
                   hole = 0.45,
                   width =250,
                   height=200)
    
    pie_chart1.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    return filters,top_table,pie_chart,dm_summary_table,pie_chart1,pie_chart1,pie_chart1,pie_chart1


# Shows and hides the Filter buttons as per the selected DM or DQ radio button
# first output will disable the filter buttons
# second output will hide the filter buttons
@main_app.app.callback(
        [Output(filter_id+"_drop_down" ,"disabled") for filter_id in main_app.environment_details['filter_ids'].split(',')],
        [Output(f"filter_card_{index}","style") for index in range(len(main_app.environment_details['filter_ids'].split(',')))],
        [Output("data_migration_dashboard","style")],
        [Output("data_quality_dashboard","style")],
        Input("filter_type","value")
)
def change_filter_buttons_and_dashboard_content(filter_type_value):
    filter_types = main_app.environment_details['filter_types'].split(',')
    output1 = [False if flag == "common" or flag == filter_type_value else True for flag in filter_types]
    output2 = [{} if flag == "common" or flag == filter_type_value else {"display":"none"} for flag in filter_types]
    styles = [{"display" : "none"},{"display" : "block"}] if filter_type_value == 'dq' else [{"display" : "block"},{"display" : "none"}]
    return output1+output2+styles

# changes the bottom table values as per the selected top table value
@main_app.app.callback(
    Output("bottom_table_container", "children"),
    Output("fig_2", "figure"),
    Output("loading_screen","style"),
    Output("bottom_table_failed_records","style",allow_duplicate=True),
    Output("bottom_table_container","style",allow_duplicate=True),
    Input({"type" : f'{main_app.environment_details["top_table_id"]}_row_number', "index" : ALL },"n_clicks"),
    State({"type" : f'{main_app.environment_details["top_table_id"]}_row_number' , 'index' : ALL},"key"),  
    State("filter_type","value"),
    prevent_initial_call = True 
)
def change_graph_and_table_data(n_clicks,key,filter_type_value):

    trigger_id = ctx.triggered_id
    sql_query = f'select * from technical_reconciliation where `Rule Name` = "{key[trigger_id["index"]]}"'
    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    table = create_dash_table_from_data_frame(
        data_frame_original=data_frame,
        table_id="bottom_table",
        key_col_number=1,
        primary_kel_column_numbers=list(map(int,main_app.environment_details["bottom_table_primary_key_column_number"].split(","))),
        action_col_numbers=[11],
        col_numbers_to_omit=[12])
    
    data_frame["In_Scope_%"] = 100
    data_frame["Success_%"] = data_frame["Success"]/data_frame["In_Scope"]*100
    data_frame["Defects_%"] = data_frame["Defects"]/data_frame["In_Scope"]*100
    line_chart_data = data_frame.melt(id_vars = ['RunID','In_Scope','Success','Defects'],value_vars=['In_Scope_%','Success_%','Defects_%'],
                        var_name='Description',value_name='Percentage')



    line_chart = px.line(data_frame = line_chart_data ,
                        height=244,
                        width=344,
                        x="RunID",
                        y='Percentage' , 
                        color = 'Description',
                        color_discrete_map = {'In_Scope_%':'blue','Success_%':'green','Defects_%':'red'}
                        )

    
    #uncomment the blow graph codes if needed

    # #converting the RunID column to string data type:
    # data_frame["RunID"] = data_frame["RunID"].astype("string")

    # pie = px.pie(data_frame= data_frame.loc[:,['RunID','In_Scope','Success','Defects']].melt(id_vars=["RunID","In_Scope"],var_name= "Success/Failre", value_name= "Count"),
    #              names = "Success/Failre",
    #              values="Count",
    #              height= 244,
    #              width= 344,
    #              title= f"{key[trigger_id['index']]} - Cumulative",
    #              color_discrete_sequence = ["green","red"]
    #             )
    
    # bar = px.bar(data_frame=data_frame,
    #     x = "RunID",
    #     y = ["Success","Defects",],
    #     color_discrete_map = {"Success":"green","Defects":"red"},
    #     title=f"{key[trigger_id['index']]} - Individual",
    #     barmode='group',
    #     height= 244,
    #     width= 344,)
    
    # bar.update_layout(legend=dict(
    # orientation="h",
    # yanchor="bottom",
    # y=-2,
    # xanchor="right",
    # x=1
    # ))

    # pie.update_layout(legend=dict(
    # orientation="h",
    # yanchor="bottom",
    # y=-1,
    # xanchor="right",
    # x=1
    # ))
    
    
    return table,line_chart,{"display":"none"},{"display" : "none"},{} # this ouput is for returning without pie chart
    # return table,bar,pie,{"display":"none"},{"display" : "none"},{}
    # return table,{"display":"none"},{"display" : "none"},{}

# for now commenting this download feature. The details will be updated later

# @main_app.app.callback(
#     Output("data_to_download","data"),
#     Input({"type" : "bottom_table_row_data","index" :  ALL},"n_clicks"),
#     State({"type" : "bottom_table_row_data","index":ALL},"key"),
#     prevent_initial_call = True
# )
# def download_data(n_clicks,key):

#     #this trigerred id is used to access the correct nclicks and key value from the array of inputs
#     trigger_id = ctx.triggered_id

#     if(n_clicks[trigger_id['index']] is None):
#         raise PreventUpdate
    
#     # print(f'n_clicks = {n_clicks}')
#     # print(f'key ===== {key}')
#     # print(f"ctx.triggered_id = {ctx.triggered_id}")
#     # print(f"ctx.triggered ===={ctx.triggered}")
#     # print(f"ctx.triggered_prop_ids ===={ctx.triggered_prop_ids}")
#     # print(f"ctx.states ===={ctx.states}")
#     # print(f"Key value for selected index is = {key[trigger_id['index']]}")

#     sample_content = f'''Downloading data column : {key[trigger_id['index']]['current_col_name']} 
#     ===================================================================== 
#     Primay keys used  : {key[trigger_id['index']]['primary_keys']}'''

#     return dict(content = sample_content,filename = "sample_download.txt")


@main_app.app.callback(
    Output("bottom_table_failed_records","children"),
    Output("bottom_table_failed_records","style",allow_duplicate=True),
    Output("bottom_table_container","style",allow_duplicate=True),
    Input({"type" : "bottom_table_row_data","index" :  ALL},"n_clicks"),
    State({"type" : "bottom_table_row_data","index":ALL},"key"),
    prevent_initial_call = True
)
def show_failed_records(n_clicks,key):

    #this trigerred id is used to access the correct nclicks and key value from the array of inputs
    trigger_id = ctx.triggered_id

    if(n_clicks[trigger_id['index']] is None or int(key[trigger_id['index']]['column_data']) == 0):
        raise PreventUpdate
    
    keys = key[trigger_id['index']]['primary_keys']
    
    #creating a sql query to show temporary failed records
    
    failure_table_name = keys[2]["FD Table"]
    no_of_failed_records = 0

    try :
        sql_query = f"select * from {failure_table_name} where `RunID` = {keys[0]['RunID']}"
        data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)
        print(sql_query)
        no_of_failed_records = len(data_frame.index)
        failed_records = create_dash_table_from_data_frame(
                            data_frame_original=data_frame,
                            table_id="failed_records",
                            key_col_number= 1,
                            capital_headings=True
                            ) if no_of_failed_records != 0 else "No failed records to display"
    except Error as e :
        if e.errno == errorcode.ER_BAD_TABLE_ERROR :
            failed_records = "No Table created in  backend for now"
        elif e.errno == errorcode.ER_SYNTAX_ERROR :
            failed_records = "Please check your SQL syntax"
        else :
            failed_records = "Something Unexpected happened please contact support"

    layout = html.Div([
        html.Div([
            html.Button(id="failed_records_header_back_button",
                        className="bi bi-arrow-left-circle btn-theme1"),
            html.Button(id="download_data_excel", 
                        className = f"bi bi-download btn-theme1 {'disabled' if no_of_failed_records == 0 else ''}",
                        disabled= True if no_of_failed_records == 0 else False),
            dcc.Input(id="data_download_query",value=sql_query,style={"display":"none"}) # this query data will be used to download the data to an excel file
        ],className="failed-records-header"),
        html.Div([
            failed_records
        ],id="failed_records_contents")
    ],className="failed-records-container")

    return layout,{},{"display" : "none"}

@main_app.app.callback(
    Output("bottom_table_failed_records","style",allow_duplicate=True),
    Output("bottom_table_container","style",allow_duplicate=True),
    Input("failed_records_header_back_button","n_clicks"),
    prevent_initial_call = True,
)
def  show_and_hide_failed_records(n_clicks):
    if (n_clicks is None):
        raise PreventUpdate
    return {"display" : "none"},{}


#Function for downloading Excel files
@main_app.app.callback(
    Output("data_to_download","data"),
    Input("download_data_excel","n_clicks"),
    State("data_download_query","value"),
    prevent_initial_call = True
)
def download_data(n_clicks,sql_query):

    if(n_clicks is None):
        raise PreventUpdate
    
    # sql_query = "select LIFNR, NAME1, NAME2, ORT01, ORT02, REGIO, STRAS, ADRNR from vw_lfa1_city_fields_blank"
    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)
  
    return dcc.send_data_frame(data_frame.to_excel, "sample_download.xlsx", sheet_name="Failed_Data")
