
#%% Run the scripts
%run database_utils.py
%run data_extraction.py
%run data_cleaning.py


#%% Connect to DB and print table names
my_connector = DatabaseConnector()
db_creds_file = "db_creds.yaml"
db_dict = my_connector.read_db_creds(db_creds_file)
db_engine = my_connector.init_db_engine()
db_table_names = my_connector.list_db_tables()
print(db_table_names)


#%% Extract the data to a dataframe
my_extractor = DataExtractor()
df = my_extractor.read_rds_table(my_connector, "legacy_users")


# %% Clean the data
my_cleaner = DataCleaning()
df = my_cleaner.clean_user_data(df)
df.info()


#%% Inspect the data (Optional)
df.head(20)


# %%
my_connector.upload_to_db(df, "dim_users")
# %%
