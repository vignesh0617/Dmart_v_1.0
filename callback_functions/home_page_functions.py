from dash.dependencies import Output, Input, State, MATCH, ALL
from dash import dcc
from callback_functions.custom_helpers import main_app
from dash.exceptions import PreventUpdate
from connections.MySQL import *
import dash_bootstrap_components as dbc
from dash import dash_table, html, ctx
from numpy import insert
from callback_functions.custom_helpers import create_dash_table_from_data_frame
import plotly.express as px

# @main_app.app.callback(
#     Output("show-hide-button","className"),
#     Output("show-hide-popover","children"),
#     Output("side-filter-tab-container","style"),
#     Output("main-content-container","style"),
#     Input("show-hide-button","n_clicks"),
#     State("show-hide-button","className"),
#     prevent_initial_call=True)
# def show_hide_filter_section(n_clicks,class_name):
#     if(n_clicks%2==1):
#         return class_name.replace("right","left"),"Hide Filters",{"left":"0px"},{"width":"70%","margin-left":"30%"}#{"width":"70%","margin-left":"30%"}
#     else:
#         return class_name.replace("left","right"),"Show Filters",{},{}


@main_app.app.callback(
    Output("side-filter-tab-container","style"),
    Output("main-content-container","style"),
    Output("clear_filter_button","style"),
    Output("apply_filter_button","style"),
    Output("filters","style"),
    Output("show-hide-button","style"),
    Input("show-hide-button","n_clicks"),
    prevent_initial_call=True)
def show_hide_filter_section(n_clicks):
    if(n_clicks%2==1):
        return {"flex-basis":"20%"},{"flex-basis":"80%"},{"opacity":"1"},{"opacity":"1"},{"opacity":"1"},{"color":"green"}
    else:
        return {},{},{},{},{},{}


@main_app.app.callback(
    Output("main-content-container","children"),
    Input("execute_query","n_clicks"),
    State("query","value")
)
def get_table_data(n_clicks,sql_query):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = get_data_as_data_frame(sql_query=sql_query, cursor= main_app.cursor)
        return dash_table.DataTable(data=df.to_dict('records'),columns=[{"name" : i, "id" : i} for i in df.columns])


@main_app.app.callback(
        Output("filters","children"),
        Output("top_table","children"),
        Input("refresh_button","n_clicks"),
)
def create_filter_buttons_figures_and_tables(n_clicks):
    filter_tables = main_app.environment_details['filter_table_names'].split(',')
    filter_tables_columns = main_app.environment_details['filter_table_columns'].split(',')
    filter_tables_labels = main_app.environment_details['filter_table_labels'].split(',')
    filter_ids = main_app.environment_details['filter_ids'].split(',')

    filters = []

    for i in range(len(filter_tables)):
        table_name = filter_tables[i]
        column_name = filter_tables_columns[i]
        column_label = filter_tables_labels[i]
        filter_id = filter_ids[i]
        
        sql_1 = f"select distinct {column_name} from {table_name}"
        data_frame = get_data_as_data_frame(sql_query=sql_1  , cursor= main_app.cursor)
        layout = html.Div([
            dbc.Label(column_label,className = "filter-label"),
            dcc.Dropdown(id = filter_id , 
                       options=data_frame[data_frame.columns[0]],
                       className = "filter-dropdown",
                       multi= True,
                       placeholder= f"Select {column_label} ... ")
        ],className = "filter-card")

        filters.append(layout)

    sql_2 = "select Max(RunID) as 'RunID', Migration_Object_Name from technical_reconciliation group by Migration_Object_Name"
    
    data_frame = get_data_as_data_frame(sql_query=sql_2,cursor=main_app.cursor)

    top_table = create_dash_table_from_data_frame(data_frame=data_frame, table_id = "run_table" , key_col_number= 1)
    
    return filters,top_table


#may be the below code can be understood and used in future

# @main_app.app.callback(
#     Output({"type" : "run_table_test" , 'index' : MATCH},"className"),
#     # Output({"type" : "home_page_contents_bottom", "index":MATCH}, "children"),
#     Input({"type" : "run_table_test" , "index" : MATCH },"n_clicks"),
#     State({"type" : "run_table_test" , 'index' : MATCH},"key"),   
#     prevent_initial_call = True 
# )
# def test(n_clicks,key):
#     if main_app.table1 is None:
#         main_app.table1 = Patch()
#         print(main_app.table1)
#     trigger_id = ctx.triggered_id
#     print(key)   
#     main_app.table1 = 1
#     return "table-active"#,main_app.table1

@main_app.app.callback(
    Output("home_page_contents_bottom", "children"),
    Output("fig_1", "figure"),
    Output("fig_2", "figure"),
    Input({"type" : "run_table" , "index" : ALL },"n_clicks"),
    State({"type" : "run_table" , 'index' : ALL},"key"),   
    prevent_initial_call = True 
)
def change_graph_and_table_data(n_clicks,key):
    trigger_id = ctx.triggered_id

    print(trigger_id)
    print(f'key ===== {key}')
    print(f"showing contents for selected Key = {key[trigger_id['index']]}")
    main_app.current_migration_object = key[trigger_id['index']]

    sql_query = f"select * from technical_reconciliation where Migration_Object_Name = '{key[trigger_id['index']]}'"
    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    table = create_dash_table_from_data_frame(
        data_frame=data_frame,table_id="bottom_table",
        key_col_number=1,
        primary_kel_column_numbers=[1,2],
        action_col_numbers=[2,3,4])
    
    #converting the RunID column to string data type:
    data_frame["RunID"] = data_frame["RunID"].astype("string")

    pie = px.pie(data_frame= data_frame.loc[:,"RunID":"Selection_Failure"].melt(id_vars=["RunID","Migration_Object_Name","In_Scope"],var_name= "Success/Failre", value_name= "Count"),
                 names = "Success/Failre",
                 values="Count",
                 height= 244,
                 width= 344,
                 title= f"{key[trigger_id['index']]} - Cumulative",
                 color_discrete_sequence = ["green","red"]
                )
    
    bar = px.bar(data_frame=data_frame,
        x = "RunID",
        y = ["Selection_Success","Selection_Failure",],
        color_discrete_map = {"Selection_Success":"green","Selection_Failure":"red"},
        title=f"{key[trigger_id['index']]} - Individual",
        barmode='group',
        height= 244,
        width= 344,)
    
    bar.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-2,
    xanchor="right",
    x=1
    ))

    pie.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-1,
    xanchor="right",
    x=1
    ))
    
    return table,bar,pie

@main_app.app.callback(
    Output("data_to_download","data"),
    Input({"type" : "bottom_table_row_data","index" :  ALL},"n_clicks"),
    State({"type" : "bottom_table_row_data","index":ALL},"key"),
    prevent_initial_call = True
)
def download_data(n_clicks,key):

    #this trigerred id is used to access the correct nclicks and key value from the array of inputs
    trigger_id = ctx.triggered_id

    if(n_clicks[trigger_id['index']] is None):
        raise PreventUpdate
    
    # print(f'n_clicks = {n_clicks}')
    # print(f'key ===== {key}')
    # print(f"ctx.triggered_id = {ctx.triggered_id}")
    # print(f"ctx.triggered ===={ctx.triggered}")
    # print(f"ctx.triggered_prop_ids ===={ctx.triggered_prop_ids}")
    # print(f"ctx.states ===={ctx.states}")
    # print(f"Key value for selected index is = {key[trigger_id['index']]}")

    sample_content = f'''Downloading data column : {key[trigger_id['index']]['current_col_name']} 
    ===================================================================== 
    Primay keys used  : {key[trigger_id['index']]['primary_keys']}'''

    return dict(content = sample_content,filename = "sample_download.txt")

