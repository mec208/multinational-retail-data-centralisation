/*
+------------------+--------------------+--------------------+
|   orders_table   | current data type  | required data type |
+------------------+--------------------+--------------------+
| date_uuid        | TEXT               | UUID               |
| user_uuid        | TEXT               | UUID               |
| card_number      | TEXT               | VARCHAR(?)         |
| store_code       | TEXT               | VARCHAR(?)         |
| product_code     | TEXT               | VARCHAR(?)         |
| product_quantity | BIGINT             | SMALLINT           |
+------------------+--------------------+--------------------+

The ? in VARCHAR is replaced with an integer 
representing the maximum length of the values in that column.
*/

SELECT * FROM orders_table;

-- date_uuid
ALTER TABLE orders_table
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid;

-- user_uuid
ALTER TABLE orders_table
ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid;

-- card_number
ALTER TABLE orders_table
ALTER COLUMN card_number TYPE TEXT
SELECT MAX(LENGTH(card_number)) AS max_length
FROM orders_table;
-- parameterise VARCHAR according to max_length
ALTER TABLE orders_table
ALTER COLUMN card_number TYPE VARCHAR(19);

-- store_code
ALTER TABLE orders_table
ALTER COLUMN store_code TYPE TEXT
SELECT MAX(LENGTH(store_code)) AS max_length
FROM orders_table;
-- parameterise VARCHAR according to max_length
ALTER TABLE orders_table
ALTER COLUMN store_code TYPE VARCHAR(12);

-- product_code
ALTER TABLE orders_table
ALTER COLUMN product_code TYPE TEXT
SELECT MAX(LENGTH(product_code)) AS max_length
FROM orders_table;
-- parameterise VARCHAR according to max_length
ALTER TABLE orders_table
ALTER COLUMN product_code TYPE VARCHAR(11);

-- product quantity
ALTER TABLE orders_table
ALTER COLUMN product_quantity TYPE SMALLINT;


-- check data types:
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'orders_table' 
AND column_name IN (
        'date_uuid',
		'user_uuid',
		'card_number',
		'store_code',
		'product_code',
		'product_quantity'
)
ORDER BY ordinal_position;

