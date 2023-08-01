
#%%
import yaml
from sqlalchemy import create_engine, inspect, text
import pandas as pd


#%%
class DatabaseConnector():
    """ Class Docstring """

    def __init__(self):
        pass

    def read_db_creds(self, db_creds_file):
        with open(db_creds_file) as f:
            self.db_creds_dict = yaml.safe_load(f)
        return self.db_creds_dict

    def init_db_engine(self):
        self.DATABASE_TYPE = 'postgresql'
        self.DBAPI = 'psycopg2'
        self.HOST = self.db_creds_dict['RDS_HOST']
        self.USER = self.db_creds_dict['RDS_USER']
        self.PASSWORD = self.db_creds_dict['RDS_PASSWORD']
        self.DATABASE = self.db_creds_dict['RDS_DATABASE']
        self.PORT = self.db_creds_dict['RDS_PORT']
        self.engine = create_engine(
            f"{self.DATABASE_TYPE}+{self.DBAPI}://"
            f"{self.USER}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/"
            f"{self.DATABASE}"
        )
        return self.engine
    
    def list_db_tables(self):
        self.inspector = inspect(self.engine)
        self.db_table_names = self.inspector.get_table_names()
        return self.db_table_names
    
    def upload_to_db(self, df_name, table_name):
        self.upload_DATABASE_TYPE = 'postgresql'
        self.upload_DBAPI = 'psycopg2'
        self.upload_HOST = 'localhost'
        self.upload_USER = 'postgres'
        self.upload_PASSWORD = 'mattpostgres'
        self.upload_DATABASE = 'sales_data'
        self.upload_PORT = 5432
        self.upload_engine = create_engine(
            f"{self.upload_DATABASE_TYPE}+{self.upload_DBAPI}://"
            f"{self.upload_USER}:{self.upload_PASSWORD}@"
            f"{self.upload_HOST}:{self.upload_PORT}/"
            f"{self.upload_DATABASE}"
        )
        self.upload_engine.connect()
        df_name.to_sql(table_name, self.upload_engine, if_exists='replace') 


