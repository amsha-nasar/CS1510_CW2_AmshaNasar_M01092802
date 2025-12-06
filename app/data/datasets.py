
from app.data.db import connect_database
import pandas as pd 
from app.data.schema import create_users_table,create_cyber_incidents_table,create_datasets_metadata_table



def get_all_data(conn):
    data=pd.read_sql_query( "SELECT * FROM metadata "  ,conn )
    return data
