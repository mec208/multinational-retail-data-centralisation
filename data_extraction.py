
import pandas as pd

class DataExtractor():
    """ Class Docstring """
    def __init__(self):
        pass

    def read_rds_table(self, connector, table_name):
        self.table_name = pd.read_sql_table(table_name, connector.engine)
        return self.table_name