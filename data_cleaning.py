

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
        # remove rows with missing data in every column
        df = df.dropna(how='all')
        # Rows with incorrect information
        # several rows have just CAPS and numbers  
        # e.g. indices 752, 1046, 2995, CA1XGS8GZW in several fields
        # identifiable because lacking '@' in email field
        mask_at_symbol_in_email = df['email_address'].str.contains('@', na=False)
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
        df[['phone', 'extension']] = (
            df['phone_number'].str.split(r'\s*x\s*|ext\s*', expand=True)
        )
        df['phone_number'] = df['phone']
        df.drop(columns='phone', inplace=True)
        return df


    def clean_card_data(self, df):  
        # Check for duplicated rows
        df.duplicated().sum()
        duplicates_mask = df.duplicated()
        # Keep only the unique rows
        df = df.loc[~duplicates_mask]
        # get rid of 'Unnamed: 0' column, since all null
        df = df.drop('Unnamed: 0', axis=1)
        # In this data frame, the word 'NULL' is used to define missing data
        df = df.replace('NULL', np.nan)
        # small number with "NULL NULL", where 2 "NULLS" concatenated
        df = df.replace('NULL NULL', np.nan)  
        # remove rows with missing data
        df = df.dropna(axis=0, how='all')
         # Separate concatenated card_number and expiry_date 
        # back into the original columns       
        mask = df['card_number expiry_date'].isnull() == False
        df[['card_temp', 'exp_temp']] = (
            df['card_number expiry_date']
            .str.split(" ", expand=True)
        )    
        df.loc[mask, 'card_number'] = df.loc[mask, 'card_temp']
        df.loc[mask, 'expiry_date'] = df.loc[mask, 'exp_temp']
        # remove the temporary columns
        df.drop(columns=[
            'card_number expiry_date',
            'card_temp',
            'exp_temp'
        ], inplace=True)
        # Invalid Entries:  
        # rows with uppercase letters and numbers in several columns
        df['expiry_date'] = df['expiry_date'].astype(str)
        invalid_entry_mask = df['expiry_date'].str.contains(r'[^0-9/]')
        df[invalid_entry_mask]
        # drop rows with invalid entries
        df = df.loc[~invalid_entry_mask]
        # Clean card numbers
        # Some card numbers are padded with ? or potentially " "
        df['card_number'] = df['card_number'].astype(str)
        non_numeric_mask = df['card_number'].str.match(r'[^0-9]', na=False)
        df['card_number'] = (
            df['card_number'].replace(r'[^0-9]', '', regex=True)
        )
        return df
    

    def clean_store_data(self, df):
        # Check for duplicated rows
        df.duplicated().sum()
        duplicates_mask = df.duplicated()
        # Keep only the unique rows
        df = df.loc[~duplicates_mask]
        # NULL values
        # in this data frame, the word 'NULL' is used to define missing data
        df = df.replace('NULL', np.nan)
        df = df.replace('N/A', np.nan) # in some rows (e.g. for webstore)
        # remove rows with missing data in every column
        df = df.dropna(how='all')
        # Rows with 'lat' values have incorrect entries for several columns        
        mask = df['lat'].isnull() == False
        df = df.loc[~mask]
        # Drop 'lat' column
        df = df.drop('lat', axis=1) 
        # Replace None type with NaN in latitude (consistent with Longitude)
        df.loc[0, 'latitude'] = np.nan
        # Convert latitude and longitude to numeric
        df['longitude'] = (
            df['longitude']
            .str.replace(r'[^\d+-.]', '', regex=True)
            .astype(float)
        )
        df['latitude'] = (
            df['latitude']
            .str.replace(r'[^\d+-.]', '', regex=True)
            .astype(float)
        )
        # Remove text characters from staff_numbers
        df['staff_numbers'] = (
            df['staff_numbers']
            .str.replace(r'[^\d]', '', regex=True)
            .astype(int)
        )
        # Correct incorrectly entered continent values
        df['continent'].value_counts()
        df['continent'] = df['continent'].str.replace('ee', '')
        # Address Issues 
        # 1. "\n" used as separator, replace with ", "
        df['address'] = df['address'].str.replace('\n', ', ')
        # 2. Title case (capitalize each word)
        df['address'] = df['address'].str.title()
        # UK postcodes
        mask = df['country_code'] == "GB"
        # Use regex to extract UK postcodes to new column
        postcode_pattern = r'\b([A-Za-z]{1,2}\d{1,2}[A-Za-z]? \d[A-Za-z]{2})\b'
        df.loc[mask, 'postcode'] = (
            df.loc[mask, 'address']
            .str.extract(postcode_pattern, expand=False)
        )
        df.loc[mask, 'postcode'] = (
            df.loc[mask, 'postcode']
            .str.upper()
        )
       # Remove postcodes from the 'text' column
        df.loc[mask, 'address'] = (
            df.loc[mask, 'address']
            .str.replace(postcode_pattern, '', regex=True)
            .str.strip()
        )
        # Replace ", ," with ","
        df.loc[mask, 'address'] = (
            df.loc[mask, 'address']
            .str.replace(", ,", ",", regex=False)
        )
        # US/DE zipcodes
        mask = df['country_code'].isin(['US', 'DE'])
        # Use regex to extract UK postcodes to new column
        postcode_pattern = r'\b(\d{5})\b'
        df.loc[mask, 'postcode'] = (
            df.loc[mask, 'address']
            .str.extract(postcode_pattern, expand=False)
        )
        df.loc[mask, 'postcode'] = (
            df.loc[mask, 'postcode'].str.upper()
        )
        # Remove postcodes from the 'text' column
        df.loc[mask, 'address'] = (
            df.loc[mask, 'address']
            .str.replace(postcode_pattern, '', regex=True)
            .str.strip()
        )
        # Replace ", ," with ","
        df.loc[mask, 'address'] = (
            df.loc[mask, 'address']
            .str.replace(", ,", ",", regex=False)
        )
        # rename 'postcode' column to reflect new contents:
        df = df.rename(columns={'postcode': 'postcode_zipcode'})
        # Opening Dates
        # temporary rename to allow use of more generalisable date code
        df = df.rename(columns={'opening_date': 'date'})
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        date_summary = {
            'min_date': df['date'].min(),
            'max_date': df['date'].max(),
            'num_valid_dates': df['date'].notnull().sum(),
            'num_invalid_dates': df['date'].isnull().sum()
        }
        for k, v in date_summary.items():
            print(k, v)
        # rename back to opening_date
        df = df.rename(columns={'date': 'opening_date'})
        # Reorder cols - specify first 5
        first_cols = ['address', 'postcode_zipcode', 
                      'locality', 'latitude', 'longitude']
        df = df[first_cols + [col for col in df.columns 
                              if col not in first_cols]]
        return df


    def convert_product_weights(self, df):
        # drop 3 rows with incorrect values
        mask = df['weight'].isin(["9GO9NZ5JTL", "MX180RYSHX", "Z8ZTDGUZVU"])
        df.drop(df[mask].index, inplace=True)
        # cleaning of incorrect values:
        df.loc[:, 'weight'] = df.loc[:, 'weight'].str.replace('77g .', '77g', regex=False)
        mask = df['product_name'].str.contains('Pleated Velvet Panel')
        df.loc[mask, 'weight'] = "1.160kg"
        # extract weight_value (last number in string) and weight units
        df.loc[:, 'weight_value'] = (
            df.loc[:, 'weight']
            .str.extract(r'([-+]?\d+\.\d+|[-+]?\d+)(?!.*\d)')
            .astype(float)
        )
        df.loc[:, 'weight_unit'] = (
            df.loc[:, 'weight']
            .str.extract(r'([a-zA-Z]+)$')
        )
        # conversion units
        unit_multipliers = {'g': 0.001, 'kg': 1.0, 'ml': 0.001, 'oz': 0.0283495}
        df.loc[:, 'kg_multiplier'] = df.loc[:, 'weight_unit'].map(unit_multipliers)
        # rows with x in are multiple items (3 x 50g or similar)  
        df.loc[:, 'multiple_item'] = df.loc[:, 'weight'].str.contains('x', na=False)
        multiple = df['weight'].str.contains('x', na=False)
        df.loc[:, 'number_of_items'] = (
            df.loc[:, 'weight']
            .str.extract(r'(\d+) x', expand=False)
            .astype(float)
        )
        df.loc[:, 'item_weight'] = (
            df.loc[:, 'weight']
            .str.extract(r'x (\d+)', expand=False)
            .astype(float)
        )
        df.loc[multiple, 'weight_value'] = (
            df.loc[multiple, 'number_of_items'] 
            * df.loc[multiple, 'item_weight']
        )
        df[multiple]
        # generate weight, retain raw weight for reference in renamed variable
        df = df.rename(columns={'weight': 'raw_weight_field'})
        df['weight'] = df['weight_value'] * df['kg_multiplier']
        # cleaning after conversion 
        # values <3g should have been listed as kg originally:
        mask = df['weight']<0.00300
        df.loc[mask, 'weight'] = df.loc[mask, 'weight']*1000
        # two specific rows clearly kg rather than g
        df.loc[1479, 'weight'] = df.loc[1479, 'weight']*1000
        df.loc[1501, 'weight'] = df.loc[1501, 'weight']*1000
        return df


    def clean_products_data(self, df):
        # remove rows with missing data in every column
        df = df.dropna(how='all')
        # Keep only the unique rows
        df.duplicated().sum()
        duplicates_mask = df.duplicated()
        df = df.loc[~duplicates_mask]
        #df.drop(df[duplicates_mask].index, inplace=True)
        return df


    def clean_orders_data(self, df):
        df = df.drop(columns = ['level_0', 'first_name', 'last_name', '1'],  axis='column')
        print(f"df.shape:               {df.shape}")
        print(f"unique values in index: {df.index.nunique()}")
        print(f"number duplicated rows: {df.duplicated().sum()}")
        return df
    

    def clean_date_data(self, df):
        df = df.replace('NULL', np.nan)
        df = df.dropna(how='all')
        print(f"df.shape:               {df.shape}")
        print(f"unique values in index: {df.index.nunique()}")
        print(f"number duplicated rows: {df.duplicated().sum()}")
        return df