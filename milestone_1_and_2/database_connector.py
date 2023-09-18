
#%%
from sqlalchemy import create_engine, inspect, text

import yaml
import pandas as pd


#%%
class DatabaseConnector():
    """ 
    Connect to Database to read or upload data 
    
    Class Methods:
    read_db_credentials: takes .yaml of credentials, returns dictionary
    init_db_engine: uses returned dictionary from read_db_credentials
                    to initialise read_engine using those credentials
    list_db_tables: uses read_engine to list tables in database
    upload_to_db: connects to PostgreSQL db, uploads DataFrame
                  with specified table name
    """

    def __init__(self):
        pass

    def read_db_creds(self, db_creds_file):
        with open(db_creds_file) as f:
            self.db_creds_dict = yaml.safe_load(f)
        return self.db_creds_dict

    def init_db_engine(self):
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = self.db_creds_dict['RDS_HOST']
        USER = self.db_creds_dict['RDS_USER']
        PASSWORD = self.db_creds_dict['RDS_PASSWORD']
        DATABASE = self.db_creds_dict['RDS_DATABASE']
        PORT = self.db_creds_dict['RDS_PORT']
        self.read_engine = create_engine(
            f"{DATABASE_TYPE}+{DBAPI}://"
            f"{USER}:{PASSWORD}@"
            f"{HOST}:{PORT}/"
            f"{DATABASE}"
        )
        return self.read_engine
    
    def list_db_tables(self):
        self.inspector = inspect(self.read_engine)
        self.db_table_names = self.inspector.get_table_names()
        return self.db_table_names
    
    def upload_to_db(self, df_name, table_name):
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'localhost'
        USER = 'postgres'
        PASSWORD = 'mattpostgres'
        DATABASE = 'sales_data'
        PORT = 5432
        self.upload_engine = create_engine(
            f"{DATABASE_TYPE}+{DBAPI}://"
            f"{USER}:{PASSWORD}@"
            f"{HOST}:{PORT}/"
            f"{DATABASE}"
        )
        self.upload_engine.connect()
        df_name.to_sql(table_name, self.upload_engine, if_exists='replace') 


