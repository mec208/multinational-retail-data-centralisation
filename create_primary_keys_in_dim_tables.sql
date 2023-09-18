SELECT * FROM orders_table;


SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'orders_table'; 


-- find out any current PRIMARY KEYS:
SELECT table_name, constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE constraint_type = 'PRIMARY KEY'
AND table_name IN (
    'dim_card_details',
    'dim_date_times',
    'dim_products',
    'dim_store_details',
    'dim_users',
    'orders_table'
)

ALTER TABLE dim_card_details
ADD CONSTRAINT pk_dim_card_details_card_number PRIMARY KEY (card_number);

ALTER TABLE dim_date_times
ADD CONSTRAINT pk_dim_date_times_date_uuid PRIMARY KEY (date_uuid);

ALTER TABLE dim_products
ADD CONSTRAINT pk_dim_products_product_code PRIMARY KEY (product_code);

ALTER TABLE dim_store_details
ADD CONSTRAINT pk_dim_store_details_store_code PRIMARY KEY (store_code);

ALTER TABLE dim_users
ADD CONSTRAINT pk_dim_users_user_uuid PRIMARY KEY (user_uuid);


-- check all added successfully:
SELECT table_name, constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE constraint_type = 'PRIMARY KEY'
AND table_name IN (
    'dim_card_details',
    'dim_date_times',
    'dim_products',
    'dim_store_details',
    'dim_users',
    'orders_table'
)