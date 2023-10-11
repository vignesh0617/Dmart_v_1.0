from dash.dependencies import Output, Input, State
from dash import no_update,ctx
from callback_functions.custom_helpers import main_app,create_dash_table_from_data_frame
import pandas as pd
import plotly.express as px
from connections.MySQL import get_data_as_data_frame
from dash.exceptions import PreventUpdate


#this function will apply the filter values to technical recon view and show the output in dashboard home page
@main_app.app.callback(
    Output("bottom_table_container", "children",allow_duplicate=True),
    # Output("fig_1", "figure",allow_duplicate=True),
    Output("fig_2", "figure",allow_duplicate=True),
    Output("bottom_table_failed_records","style",allow_duplicate=True),
    Output("bottom_table_container","style",allow_duplicate=True),
    Output("data_migration_bottom_table","children",allow_duplicate=True),
    Output("fig_3", "figure",allow_duplicate=True),
    Output("fig_4", "figure",allow_duplicate=True),
    Output("fig_5", "figure",allow_duplicate=True),
    Output("fig_6", "figure",allow_duplicate=True),
    Input("apply_filter_button","n_clicks"),
    State("filter_type","value"),
    [State(filter_id,"value") for filter_id in main_app.environment_details['filter_ids'].split(',')],
    prevent_initial_call = True 
)
def change_table_and_graph_data_for_technical_recon_view(n_clicks,filter_type,*filter_values):

    # if(filter_type == 'dq'):
    #     raise PreventUpdate


    if(filter_type == 'dq'):
        table = None
        # pie = px.bar()
        # bar = px.bar()
        line_chart = px.line()

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
                data_frame_original=data_frame,
                table_id="bottom_table",
                key_col_number=1,
                primary_kel_column_numbers=list(map(int,main_app.environment_details["bottom_table_primary_key_column_number"].split(","))),
                action_col_numbers=[11],
                col_numbers_to_omit=[12])
            
            data_frame["RunID"] = data_frame["RunID"].astype("string")

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
                
        else :
            table = "No contents found for the applied filter"
        
        print("-------------------Filter Applied-----------------")
        print(sql_query)

        return table,line_chart,{"display":"none"},{},no_update,no_update,no_update,no_update,no_update
        # return table,line,pie,{"display":"none"},{}

    elif(filter_type == 'dm'):

        table = None

        filter_columns = main_app.environment_details['filter_table_columns'].split(',')

        dictionary = dict([filter_columns[index],filter_values[index]] for index,value in enumerate(filter_values))

        sql_query = f"select * from DM_Summary"

        filter_types = main_app.environment_details['filter_types'].split(',')

        index = 0
        for column_name,filter_value in dictionary.items():
            if(filter_value is not None):
                if(len(filter_value)!=0 and (filter_types[index] == "common" or  filter_types[index] == filter_type )) :
                    sql_query+=f" {' and ' if sql_query.find('where')!=-1 else ' where '} {column_name} in {filter_value} "
            index+=1

        sql_query = sql_query.replace("[","(").replace("]",")")

        data_frame = get_data_as_data_frame(sql_query=sql_query,cursor=main_app.cursor)

        if(len(data_frame != 0)):
            dm_summary_table = create_dash_table_from_data_frame(
                data_frame_original=data_frame,
                table_id="data_migration_bottom_table_contents",
                key_col_number=1,
                # primary_kel_column_numbers=list(map(int,main_app.environment_details["bottom_table_primary_key_column_number"].split(","))),
                # action_col_numbers=[11],
                # col_numbers_to_omit=[12]
                )

            
        else :
            dm_summary_table = "No contents found for the applied filter"
        
        print("-------------------Filter Applied-----------------")
        print(sql_query)

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

        return no_update,no_update,no_update,no_update,dm_summary_table,pie_chart1,pie_chart1,pie_chart1,pie_chart1
        # return table,line,pie,{"display":"none"},{}


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



