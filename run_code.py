
#%% Run the scripts
%run database_utils.py
%run data_extraction.py
%run data_cleaning.py


#%%
# Initialise the Classes
my_connector = DatabaseConnector()
my_extractor = DataExtractor()
my_cleaner = DataCleaning()


#%% 
# Connect to Amazon RDS DB for User and Orders Data

# Connect to user DB and print table names
db_creds_file = "db_creds.yaml"
db_dict = my_connector.read_db_creds(db_creds_file)
db_engine = my_connector.init_db_engine()
db_table_names = my_connector.list_db_tables()
print(db_table_names)



##################################################################
#%% 
# User Data

# Extract the User data to a Pandas dataframe
user_df = my_extractor.read_rds_table(my_connector, "legacy_users")
user_df.info()

#%% 
# Clean the user data
user_df = my_cleaner.clean_user_data(user_df)
user_df.info()


# %% Upload Cleaned User Data to Postgresql DB 
my_connector.upload_to_db(user_df, "dim_users")




##################################################################
# #%% 
# Card Data

# Extract the Card data from a PDF at the URL below
# Store in a Pandas dataframe

card_df = my_extractor.retrieve_pdf_data(
    "https://data-handling-public.s3.eu-west-1.amazonaws.com/"
    "card_details.pdf"
)
card_df.info()


# %% Clean the Card Data
card_df = my_cleaner.clean_card_data(card_df)
card_df.info()


# %% Upload Card data to Postgresql DB 
my_connector.upload_to_db(card_df, "dim_card_details")


##################################################################
#%% 
# Store Data

# Number of stores
endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"
}

# Extract and list the number of stores
number_of_stores = my_extractor.list_number_of_stores(endpoint, headers)
print(number_of_stores)

#%%
# Store Details
endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/"
headers = {
            "Content-Type": "application/json",
            "x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"
        }

# Extract the Stores Data to a DataFrame
stores_df = my_extractor.retrieve_stores_data(endpoint, headers, number_of_stores)
stores_df

#%% 
# Clean the Stores Data
stores_df = my_cleaner.clean_store_data(stores_df)
stores_df.info()

#%%
# Upload the Stores Data to PostgreSQL DB
my_connector.upload_to_db(stores_df, "dim_store_details")



##################################################################
# %%
# Product Data

# Extract the Products Data from the S3 Bucket, return DataFrame
s3_url = "s3://data-handling-public/products.csv"
products_df = my_extractor.extract_from_s3(s3_url)

#%%
# Clean the Products Data
products_df = my_cleaner.clean_products_data(products_df)
products_df.info()

#%%
# Convert the Product Weights to kg
products_df = my_cleaner.convert_product_weights(products_df)
products_df.info()

#%% 
# Upload Product data to PostgreSQL DB.
my_connector.upload_to_db(products_df, "dim_products")
# %%



##################################################################
#%%
# Orders Data


#%%
# Get names of the tables in the Amazon RDS DB
inspector = inspect(db_engine)
inspector.get_table_names()

# check columns in the orders table
column_list = inspector.get_columns("orders_table")
for column in column_list:
    print(column['name'])


#%%
# Extract the Orders data to a Pandas dataframe
orders_df = my_extractor.read_rds_table(my_connector, "orders_table")
orders_df.info()


#%%
# Clean the Order Data
orders_df = my_cleaner.clean_orders_data(orders_df)
orders_df.info()

#%%
# Upload Order Data to DB
my_connector.upload_to_db(orders_df, "orders_table")


#####################################################################
# %%
# Date Data

# Extract Date Data from JSON file using Context manager:

url = (
    "https://data-handling-public.s3.eu-west-1.amazonaws.com/"
    "date_details.json"
)
print(url)

dates_df = my_extractor.retrieve_date_data(url)
dates_df.info()

# %% 
# Clean Date Data
dates_df = my_cleaner.clean_date_data(dates_df)
dates_df.info()



#%%
# Upload Dates Data to DB
my_connector.upload_to_db(dates_df, "dim_date_times")


#####################################################################
