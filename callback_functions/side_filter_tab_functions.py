from dash.dependencies import Output, Input, State
from dash import no_update,ctx
from callback_functions.custom_helpers import main_app,create_dash_table_from_data_frame
import pandas as pd
import plotly.express as px
from connections.MySQL import get_data_as_data_frame
from dash.exceptions import PreventUpdate


#this function will apply the filter values to technical recon view and show the output in dashboard home page
@main_app.app.callback(
    Output("bottom_table", "children",allow_duplicate=True),
    Output("fig_1", "figure",allow_duplicate=True),
    Output("fig_2", "figure",allow_duplicate=True),
    Output("bottom_table_failed_records","style",allow_duplicate=True),
    Output("bottom_table","style",allow_duplicate=True),
    Input("apply_filter_button","n_clicks"),
    State("filter_type","value"),
    [State(filter_id,"value") for filter_id in main_app.environment_details['filter_ids'].split(',')],
    prevent_initial_call = True 
)
def change_table_and_graph_data_for_technical_recon_view(n_clicks,filter_type,*filter_values):

    if(filter_type == 'dm'):
        raise PreventUpdate


    table = None
    pie = px.bar()
    bar = px.bar()

    filter_columns = main_app.environment_details['filter_table_columns'].split(',')

    dictionary = dict([filter_columns[index],filter_values[index]] for index,value in enumerate(filter_values))

    sql_query = f"select * from technical_reconciliation"

    filter_types = main_app.environment_details['filter_types'].split(',')

    index = 0
    for column_name,filter_value in dictionary.items():
        if(filter_value is not None):
            if(len(filter_value)!=0 and (filter_types[index] == "common" or  filter_types[index] == filter_type )) :
                sql_query+=f" {' and ' if sql_query.find('where')!=-1 else ' where '} {column_name} in {filter_value} "
        index+=1

    sql_query = sql_query.replace("[","(").replace("]",")")

    # print(f"SQL Query =========== \n\n\n\n{sql_query}\n\n\n\n")

    data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

    if(len(data_frame != 0)):
        table = create_dash_table_from_data_frame(
            data_frame_original=data_frame,table_id="bottom_table",
            key_col_number=1,
            primary_kel_column_numbers=list(map(int,main_app.environment_details["bottom_table_primary_key_column_number"].split(","))),
            action_col_numbers=[11],
            col_numbers_to_omit=[12])
        
        data_frame["RunID"] = data_frame["RunID"].astype("string")

        pie = px.pie(data_frame= data_frame.loc[:,['RunID','In_Scope','Success','Defects']].melt(id_vars=["RunID","In_Scope"],var_name= "Success/Failre", value_name= "Count"),
                names = "Success/Failre",
                    values="Count",
                    height= 244,
                    width= 344,
                    title= f"Cumulative",
                    color_discrete_sequence = ["green","red"]
                    )
        
        bar = px.bar(data_frame=data_frame,
            x = "RunID",
            y = ["Success","Defects",],
            color_discrete_map = {"Success":"green","Defects":"red"},
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
    
    print("-------------------Filter Applied-----------------")
    print(sql_query)
    return table,bar,pie,{"display":"none"},{}

@main_app.app.callback(
    # [Output(filter_id+"_select_all","value") for filter_id in main_app.environment_details["filter_ids"].split(",")],
    [Output(filter_id,"value") for filter_id in main_app.environment_details["filter_ids"].split(",")],
    Input("clear_filter_button","n_clicks"),
    prevent_initial_call=True
)
def clear_all_filters(n_clicks):
    return [[] for filter_id in main_app.environment_details["filter_ids"].split(",")]




#The below loop is used to update the labels of each filter passed
filter_ids = main_app.environment_details['filter_ids'].split(',')

for i in range(len(filter_ids)):
    filter_id = filter_ids[i]
    
    #trying to implement a new feature
    @main_app.app.callback(
        Output(filter_id+"_drop_down","label"),
        Output(filter_id+"_select_all","value"),
        Input(filter_id,"value"),
        State(filter_id,"options"),
        # prevent_initial_call='initial_duplicate',
        # State(filter_id+"_select_all","value"),
    )
    def update_filter_label_and_options(value,options):
        
        print(f"***********************line 128 side filter table functions {filter_id}")
        if(len(value)==len(options)):
            return "All",True
        return str([item for item in value]).replace("[","").replace("]","").replace("'","") if len(value) !=0 else "None", None

    @main_app.app.callback(
        Output(filter_id+"_drop_down","label",allow_duplicate=True),
        Output(filter_id,"value",allow_duplicate=True),
        Input(filter_id+"_select_all","value"),
        State(filter_id,"options"),
        prevent_initial_call='initial_duplicate',
    )
    def update_filter_label_and_options(selected,options):
            if selected == None :
                raise PreventUpdate
            if selected :
                return "All",[item for item in options]
            else :
                return "None",[]


#trying to implement a new feature
# @main_app.app.callback(
#     Output("migration_Object_f"+"_drop_down","label"),
#     Output("migration_Object_f"+"_select_all","value"),
#     Input("migration_Object_f","value"),
#     State("migration_Object_f","options"),
#     # prevent_initial_call='initial_duplicate',
#     # State(filter_id+"_select_all","value"),
# )
# def update_filter_label_and_options(value,options):

#     if(len(value)==len(options)):
#         return "All",True
#     return str([item for item in value]).replace("[","").replace("]","").replace("'","") if len(value) !=0 else "None", None

# @main_app.app.callback(
#     Output("migration_Object_f"+"_drop_down","label",allow_duplicate=True),
#     Output("migration_Object_f","value",allow_duplicate=True),
#     Input("migration_Object_f"+"_select_all","value"),
#     State("migration_Object_f","options"),
#     prevent_initial_call='initial_duplicate',
# )
# def update_filter_label_and_options(selected,options):
    
#     if selected == None :
#         raise PreventUpdate
#     if selected :
#         return "All",[item for item in options]
#     else :
#         return "None",[]



