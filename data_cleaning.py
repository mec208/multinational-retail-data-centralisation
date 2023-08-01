

#%%
import pandas as pd
import numpy as np
import re
from itables import show


#%%
class DataCleaning():
    """ Class Docstring """
    def __init__(self):
        pass

    def clean_user_data(self, df):    
        # NULL values
        # in this data frame, the word 'NULL' is used to define missing data
        df = df.replace('NULL', np.nan)
        # remove rows with missing data
        df = df.dropna()

        # Rows with incorrect information
        # several rows have just CAPS and numbers  
        # e.g. indices 752, 1046, 2995, CA1XGS8GZW in several fields
        # identifiable because lacking '@' in email field
        mask_at_symbol_in_email = df['email_address'].str.contains('@')
        df = df.loc[mask_at_symbol_in_email]

        # Date
        # convert dates to datetime using pandas
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
        df['join_date'] = pd.to_datetime(df['join_date'])
        # then specify uniform display format
        df['date_of_birth'] = df['date_of_birth'].dt.strftime('%d-%m-%Y')
        df['join_date'] = df['join_date'].dt.strftime('%d-%m-%Y')

        # Address Issues 
        # 1. "\n" used as separator, replace with ", "
        df['address'] = df['address'].str.replace('\n', ', ')
        # 2. Title case (capitalize each word)
        df['address'] = df['address'].str.title()
        
        # Country Code 
        # Correct wrong entries in country code
        mask = df['country_code'] == "GGB"
        df.loc[mask, 'country_code'] = "GB"
        df['country_code'].value_counts()

        # Use the 'map' method to create a new column with merged numeric values
        country_code_dictionary = {'US': 1, 'GB': 44, 'DE': 49}
        df['numeric_country_code'] = df['country_code'].map(country_code_dictionary)
        
        # Phone Numbers
        # Remove country prefixes
        df['phone_number'] = df['phone_number'].str.replace("+1", "", regex=False)
        df['phone_number'] = df['phone_number'].str.replace("+44", "", regex=False)
        df['phone_number'] = df['phone_number'].str.replace("+49", "", regex=False)
        # Remove parentheses, full stops / periods, dashes, blanks
        df['phone_number'] = df['phone_number'].str.replace("(", "", regex=False)
        df['phone_number'] = df['phone_number'].str.replace(")", "", regex=False)
        df['phone_number'] = df['phone_number'].str.replace(".", "", regex=False)
        df['phone_number'] = df['phone_number'].str.replace("-", "", regex=False)
        df['phone_number'] = df['phone_number'].str.replace(" ", "", regex=False)

        # Split Extensions to separate variable 
        df[['phone', 'extension']] = df['phone_number'].str.split(r'\s*x\s*|ext\s*', expand=True)
        df['phone_number'] = df['phone']
        df.drop(columns='phone', inplace=True)

        return df



