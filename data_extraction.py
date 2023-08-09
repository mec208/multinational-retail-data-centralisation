
import pandas as pd
import tabula
import requests
import boto3
import os


class DataExtractor():
    """ Class Docstring """
    def __init__(self):
        pass

    def read_rds_table(self, connector, table_name):
        self.table_name = pd.read_sql_table(table_name, connector.engine, index_col = 'index')
        return self.table_name
    
    def retrieve_pdf_data(self, pdf_path):
        self.df_pages_from_pdf = tabula.read_pdf(pdf_path, stream=True, pages='all')
        self.df_from_pdf = pd.concat(self.df_pages_from_pdf)
        return self.df_from_pdf

    def list_number_of_stores(self, endpoint, headers):
        self.response = requests.get(endpoint, headers=headers)
        self.number_of_stores_dict = self.response.json()
        self.number_of_stores = self.number_of_stores_dict['number_stores']
        return self.number_of_stores
    
    def retrieve_stores_data(self, endpoint, headers, number_of_stores):
        # initialise empty list of stores
        self.stores_list = []
        # loop through a list of all the store numbers from 
        # list_number_of_stores()
        for store_number in range(0, number_of_stores):
            self.url = f"{endpoint}{store_number}"
            self.response = requests.get(self.url, headers=headers)
            self.store_dict = self.response.json()
            self.stores_list.append(self.store_dict)

        self.stores_df = pd.DataFrame(self.stores_list)
        self.stores_df = self.stores_df.set_index('index')
        return self.stores_df

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
    
