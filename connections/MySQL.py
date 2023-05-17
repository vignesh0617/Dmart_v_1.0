import mysql.connector as sql
from callback_functions.custom_helpers import main_app
import pandas as pd

#creates a backend connection with mysql connector and return the connection
def get_connection(username,password):
    try:
        connector = sql.connect(
            user = username, 
            password = password, 
            host = main_app.environment_details['host'] , 
            database = main_app.environment_details["database_name"],
            autocommit =True)
        return connector,connector.cursor(),True
    except Exception as e:
        print(f"Something Unexpected happened inside MySQL: {e}")
        return None,None,False
    
#gets tables data and returns it from the selected database as a dataframe obj
def get_data_as_data_frame(sql_query,cursor):
    cursor.execute(sql_query)
    fields = cursor.description
    data = cursor.fetchall()
    column_labels = [row[0] for row in fields]
    return pd.DataFrame(data = data, columns= column_labels)







