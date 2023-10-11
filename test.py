import pandas as pd
import mysql.connector as sql

connector =  sql.connnect(username = "root", password = "root" , host = "localhost", database = "dmart")

df = pd.read_sql(sql = "select * from dqsteward")

378867