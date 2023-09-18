
## Table of Contents

- [Milestones 1 and 2](#Milestones1and2)
- [Milestone 3](#Milestone3)

<a name="Milestones1and2"></a>
# Milestones 1 and 2
&nbsp;
## Set up PostgreSQL Database for cleaned data
A PostgreSQL database was set up to host the cleaned sales data. 

&nbsp;
## Develop three classes for processing the data
Three classes were developed, to carry out the necessary tasks related to processing of the raw data.

### `DatabaseConnector` 

This includes methods for two stages of the data processing pipeline: 
1. connection to source databases containing the raw data, allowing exploration of the tables in the source database and extraction of the data (see below)
2. uploading cleaned data to the PostgreSQL database.



### `DataExtractor`

This includes methods to extract data from the different data sources. 

Extraction makes use of a `DatabaseConnector` where necessary.  

In some cases (where data are not held in a database requiring credentials, for example), extraction can take place directly.

All extraction methods return a Pandas DataFrame for further processing.



### `DataCleaning`

This class contains methods to clean raw data prior to uploading.  

General tasks include identifying duplicate rows, identifying placeholders in the data representing missing values, identifying and removing rows where all columns are missing data, and removing rows containing unambiguous data entry errors.  

Details of data cleaning specific to different data sources are given in the relevant sections below.

&nbsp;
## User Data
User data was extracted from an Amazon RDS database. 

This requires an instance of a `DatabaseConnector` to supply the necessary credentials held in a `.yaml` file, and to list the tables in the source data.

The `read_rds_table` method in the `DataExtractor` was used to extract the data from the user table to a Pandas DataFrame.

Key `DataCleaning` tasks for user data include:
- cleaning and processsing of dates into a standard format
- cleaning and standardisation of phone numbers from three countries into a standard format (separating country prefix and the in-country number)
- processing of address data to remove line separation characters that had not formatted correctly in the text field
- extraction of postcodes / zipcodes from the address column to a separate column, accounting for country-specific conventions.

&nbsp;
## Card Data
Card data was available from a PDF held in an Amazon S3 bucket (and available directly through a URL).

The `retrieve_pdf_data` method in the `DataExtractor` extract the data from each page of the PDF using the `tabula` module, and combine these into a single DataFrame.  

Key `DataCleaning` tasks for card data include:
- separation of incorrectly concatenated data (card number and expiry date) back into separate columns
- removal of text characters and white space used to pad card numbers, to allow conversion of the column to numeric.

&nbsp;
## Store Data
Store data was available from an API. 

Two get methods of the API were used within the `DataExtractor`.  These use the `requests` module.

The first get method, implemented by the method `list_number_of_stores` returns the number of stores. The second method `retrieve_stores_data` returns the data for each store, using the response from the first method to parameterise a loop, and then combine these into a single DataFrame.

Key `DataCleaning` tasks for store data include:
- correction of latitude and longitude data for each store, and conversion of these to numeric variables.
- processing of opening date from text into a date variable with standardised formatting
- extraction of postcodes / zipcodes from the address column to a separate column, accounting for country-specific conventions.

&nbsp;
## Product Data
Raw product data was held in an S3 bucket.

The `extract_from_s3` method in `DataExtractor` uses the `boto3` module to download the file to the local folder and return a DataFrame. The `os` module is used to handle the local file paths.

Generic `DataCleaning` tasks are handled with `clean_products_data`.  

A specific cleaning task for products was to `convert_product_weights`.  This requires 
- extraction of the unit of measure and the value of that unit into separate columns
- conversion of the returned `weight` of the product standardised to kg, using a conversion mapping for other units of measure (g, oz, ml).
- some products are 'multiple items', where the weight of the product is listed as "3 x 50g" or similar.  In these cases, the `number_of_items` and the `item_weight` was determined by parsing the weight string to separate these elements, and the total weight of the product (the arithmetic product of these two values, converted to kg) was returned in the `weight` column.

&nbsp;
## Orders Data
Order data was also extracted from the Amazon RDS database holding user data. 

This requires an instance of a `DatabaseConnector` to supply the necessary credentials held in a `.yaml` file, and to list the tables in the source data.

The `read_rds_table` method in the `DataExtractor` was used to extract the data from the order table to a Pandas DataFrame.

Order data are held as the 'single source of truth' for these data, and thus minimal cleaning was necessary (or desirable).  

`DataCleaning` tasks for orders data were therefore limited to checking for duplicate entries, removing empty or duplicated columns, and removing personal data (customer names).

&nbsp;
## Date Events Data 

Date events data were held in a `.json` file in an S3 bucket.

The `retrieve_date_data` method in `DataExtractor` was used to extract these data and return a DataFrame.

`DataCleaning` tasks involved creating a `datetime` object from 4 columns (timestamp, year, month, day) after removing rows where text had been entered in these columns in error.

&nbsp;
<a name="Milestone3"></a>
# Milestone 3

After the cleaned data was uploaded to the PostgreSQL database, the data base was edited as below:

### Casting columns to correct data types

Key variables were cast to specific types as required. The full list of changes is documented in the files with the prefix 'correct_data_types_in...', for each of the 6 tables in the database.

- UUID variables were cast to UUID format.
- Date variables to DATE format.
- Numeric variables to FLOAT
- In several instances, text variables were cast to the character-varying (VARCHAR) type. The maximum length of all the observations in that column was first determined, and the maximum length then used to specify the maximum number of characters.

## Data manipulation in the products table

Product prices were previously held as strings, with the '£' character as a prefix. This was stripped to allow conversion of the price to numeric.

A human-readable 'weight class' variable was created from the calculated product weight, to aid decisions about delivery weights.

## Creation of the star-based database schema

The orders table is the central **Fact table**, with order tables as **Dimension tables**.

Primary keys in the Dimension tables were created as follows:

| Dimension Table   | Dimension Table Name    | Primary Key       | 
|-------------------|-------------------------|-------------------|
| Card Details      | `dim_card_details`      | `card_number`     |
| Dates/Times       | `dim_date_times`        | `date_uuid`       |
| Products          | `dim_products`          | `product_code`    |
| Store Details     | `dim_store_details`     | `store_code`      |
| Users             | `dim_users`             | `user_uuid`       |


To complete the Star-based database schema, the Primary Keys in the above Dimension Tables were listed as Foreign Keys in the `orders_table`, referring to the appropriate dimension table.
