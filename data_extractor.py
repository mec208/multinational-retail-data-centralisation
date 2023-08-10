
import pandas as pd
import tabula
import requests
import boto3
import os


class DataExtractor():
    """ 
    Extract Data from Databases (using DatabaseConnector()) or directly
    
    Class Methods:
    read_rds_table: Return Dataframe from SQL table using DatabaseConnector()
    retrieve_pdf_data: Return Dataframe from PDF, using tabula
    list_number_of_stores: Uses requests to get number of stores from API
    retrieve_stores_data: requests data from each store from API, 
                          concatenates to single DataFrame
    extract_from_s3: parses S3 bucket URL into bucket name and filename
                     downloads filename, returns DataFrame
    retrieve_date_data: requests .json file, returns DataFrame
    """
    def __init__(self):
        pass

    def read_rds_table(self, connector, table_name):
        df = pd.read_sql_table(
            table_name, 
            connector.read_engine, 
            index_col = 'index'
    )
        return df
    
    def retrieve_pdf_data(self, pdf_path):
        self.df_pages = tabula.read_pdf(
            pdf_path, 
            stream=True, 
            pages='all'
        )
        df = pd.concat(self.df_pages)
        return df

    def list_number_of_stores(self, endpoint, headers):
        response = requests.get(endpoint, headers=headers)
        number_of_stores_dict = response.json()
        number_of_stores = number_of_stores_dict['number_stores']
        return number_of_stores
    
    def retrieve_stores_data(self, endpoint, headers, number_of_stores):
        # initialise empty list of stores
        stores_list = []
        # loop through a list of all the store numbers from 
        # list_number_of_stores()
        for store_number in range(0, number_of_stores):
            url = f"{endpoint}{store_number}"
            response = requests.get(url, headers=headers)
            store_dict = response.json()
            stores_list.append(store_dict)
        stores_df = pd.DataFrame(stores_list)
        stores_df = stores_df.set_index('index')
        return stores_df

    def extract_from_s3(self, s3_url):
        # Create a list from the URL:
        # Remove the 's3://' prefix, then 
        # split the remaining URL into bucket name and file key
        url_list = s3_url.replace("s3://", "").split('/')
        bucket_name = url_list[0]
        file_name = url_list[1]
        # Initialize S3 client
        s3 = boto3.client('s3')
        # Get the current working directory
        current_directory = os.getcwd()
        # Combine it with the filename to create the output path
        output_path = os.path.join(current_directory, file_name)
        # Download the file from S3 to the current directory
        s3.download_file(bucket_name, file_name, output_path)
        print(f"Successfully downloaded {s3_url} to {output_path}")
        # create dataframe from .csv and return it
        df = pd.read_csv(output_path)
        df = df.rename(columns={'Unnamed: 0': 'index'})
        df = df.set_index('index')
        return df
    
    def retrieve_date_data(self, url):
        with requests.get(url) as response:
            json_data = response.json()  
            df = pd.DataFrame(json_data)
        return df  
    
