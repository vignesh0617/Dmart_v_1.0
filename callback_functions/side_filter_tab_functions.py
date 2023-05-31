from dash.dependencies import Output, Input, State
from dash import no_update,ctx
from callback_functions.custom_helpers import main_app,create_dash_table_from_data_frame
import pandas as pd
import plotly.express as px
from connections.MySQL import get_data_as_data_frame

@main_app.app.callback(
    Output("home_page_contents_bottom", "children",allow_duplicate=True),
    Output("fig_1", "figure",allow_duplicate=True),
    Output("fig_2", "figure",allow_duplicate=True),
    Input("apply_filter_button","n_clicks"),
    State("migration_Object_f","value"),
    State("process_area_f","value"),
    State("environment_f","value"),
    State("rollout_f","value"),
    State("country_f","value"),   
    prevent_initial_call = True 
)
def change_graph_and_table_data(n_clicks,migration_objects,process_areas,environments,rollouts,countries):

    table = None
    pie = px.line()
    bar = px.bar()

    sql_query = f"select * from technical_reconciliation"


    if (migration_objects) is not None:
        if len(migration_objects) != 0:
            sql_query += f" where Migration_Object_Name in {migration_objects} "

    if (process_areas) is not None:
        if len(process_areas) != 0:
            sql_query += f" {'and' if sql_query.find('where')!=-1 else 'where'} Process_Area in {process_areas} "

    if (environments) is not None:
        if len(environments) != 0:
            sql_query += f" {'and' if sql_query.find('where')!=-1 else 'where'} Environment in {environments} "

    if (rollouts) is not None:
        if len(rollouts) != 0:
            sql_query += f" {'and' if sql_query.find('where')!=-1 else 'where'} Rollout in {rollouts} "
    
    if (countries) is not None:
        if len(countries) != 0:
            sql_query += f" {'and' if sql_query.find('where')!=-1 else 'where'} Process_Area in {countries} "

    sql_query = sql_query.replace("[","(").replace("]",")")
    print(f"SQL Query =========== \n\n\n\n{sql_query}\n\n\n\n")

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
