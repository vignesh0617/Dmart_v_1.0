import mysql.connector as sql
from callback_functions.custom_helpers import main_app

def get_connection(username,password):
    try:
        connector = sql.connect(user = username, password = password, host = main_app.environment_details['host'])
        return connector,True
    except Exception as e:
        print(f"Something Unexpected happened inside MySQL: {e}")
        return None,False


