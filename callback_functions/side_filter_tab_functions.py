from dash.dependencies import Output, Input, State
from dash import no_update,ctx
from callback_functions.custom_helpers import main_app,create_dash_table_from_data_frame
import pandas as pd
import plotly.express as px
from connections.MySQL import get_data_as_data_frame


#this function will apply the filter values to technical recon view and show the output in dashboard home page
@main_app.app.callback(
    Output("home_page_contents_bottom", "children",allow_duplicate=True),
    Output("fig_1", "figure",allow_duplicate=True),
    Output("fig_2", "figure",allow_duplicate=True),
    Input("apply_filter_button","n_clicks"),
    [State(filter_id,"value") for filter_id in main_app.environment_details['filter_ids'].split(',')],
    prevent_initial_call = True 
)
def change_table_and_graph_data_for_technical_recon_view(n_clicks,*filter_values):

    table = None
    pie = px.bar()
    bar = px.bar()

    filter_columns = main_app.environment_details['filter_table_columns'].split(',')

    dictionary = dict([filter_columns[index],filter_values[index]] for index,value in enumerate(filter_values))

    sql_query = f"select * from technical_reconciliation"

    for column_name,filter_value in dictionary.items():
        if(filter_value is not None):
            if(len(filter_value)!=0):
                sql_query+=f" {' and ' if sql_query.find('where')!=-1 else ' where '} {column_name} in {filter_value} "

    sql_query = sql_query.replace("[","(").replace("]",")")

    # print(f"SQL Query =========== \n\n\n\n{sql_query}\n\n\n\n")

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    if(len(data_frame != 0)):
        table = create_dash_table_from_data_frame(
            data_frame=data_frame,table_id="bottom_table",
            key_col_number=1,
            primary_kel_column_numbers=[1,2],
            action_col_numbers=[2,3,4])
        
        data_frame["RunID"] = data_frame["RunID"].astype("string")

        pie = px.pie(data_frame= data_frame.loc[:,"RunID":"Selection_Failure"].melt(id_vars=["RunID","Migration_Object_Name","In_Scope"],var_name= "Success/Failre", value_name= "Count"),
                    names = "Success/Failre",
                    values="Count",
                    height= 244,
                    width= 344,
                    title= f"Cumulative",
                    color_discrete_sequence = ["green","red"]
                    )
        
        bar = px.bar(data_frame=data_frame,
            x = "RunID",
            y = ["Selection_Success","Selection_Failure",],
            color_discrete_map = {"Selection_Success":"green","Selection_Failure":"red"},
            title=f"Individual",
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
    else :
        table = "No contents found for the applied filter"
    
    return table,bar,pie

@main_app.app.callback(
    [Output(filter_id,"value") for filter_id in main_app.environment_details["filter_ids"].split(",")],
    Input("clear_filter_button","n_clicks"),
    prevent_initial_call=True
)
def clear_all_filters(n_clicsk):
    return [[] for filter_id in main_app.environment_details["filter_ids"].split(",")]