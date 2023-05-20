from dash.dependencies import Output, Input, State, MATCH, ALL
from dash import Patch
from callback_functions.custom_helpers import main_app
from dash.exceptions import PreventUpdate
from connections.MySQL import *
import dash_bootstrap_components as dbc
from dash import dash_table, html, ctx
from numpy import insert
from callback_functions.custom_helpers import create_dash_table_from_data_frame

@main_app.app.callback(
    Output("show-hide-button","className"),
    Output("show-hide-popover","children"),
    Output("side-filter-tab-container","style"),
    Output("main-content-container","style"),
    Input("show-hide-button","n_clicks"),
    State("show-hide-button","className"),
    prevent_initial_call=True)
def toggle_buttons(n_clicks,class_name):
    if(n_clicks%2==1):
        return class_name.replace("right","left"),"Hide Filters",{"left":"0px"},{"width":"70%","margin-left":"30%"}
    else:
        return class_name.replace("left","right"),"Show Filters",{},{}
    
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
def create_filter_buttons(n_clicks):
    filter_tables = main_app.environment_details['filter_table_names'].split(',')
    filter_tables_columns = main_app.environment_details['filter_table_columns'].split(',')
    filters = []

    for i in range(len(filter_tables)):
        table_name = filter_tables[i]
        column_name = filter_tables_columns[i]
        sql_1 = f"select distinct {column_name} from {table_name}"
        data_frame = get_data_as_data_frame(sql_query=sql_1  , cursor= main_app.cursor)
        layout = html.Div([
            dbc.Label(column_name.title(),className = "filter-label"),
            dbc.Select(id = column_name , options=insert(data_frame[data_frame.columns[0]].unique(),0,'--None--'),value= '--None--',className = "filter-dropdown")
        ],className = "filter-card")

        filters.append(layout)

    sql_2 = "select Max(RunID) as 'RunID', Migration_Object_Name from technical_reconciliation group by Migration_Object_Name"
    data_frame = get_data_as_data_frame(sql_query=sql_2,cursor=main_app.cursor)

    table1 = create_dash_table_from_data_frame(data_frame=data_frame, table_id = "run_table" , key_col_number= 1)

    return filters,table1


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
    Input({"type" : "run_table" , "index" : ALL },"n_clicks"),
    State({"type" : "run_table" , 'index' : ALL},"key"),   
    prevent_initial_call = True 
)
def test(n_clicks,key):
    trigger_id = ctx.triggered_id

    return f"showing contents for selected Key = {key[trigger_id['index']]}"
