/*
as per instructions, the 'removed' column is renamed to 
'still_available' before changing its data type.

+-----------------+--------------------+--------------------+
|  dim_products   | current data type  | required data type |
+-----------------+--------------------+--------------------+
| product_price   | TEXT               | FLOAT              |
| weight          | TEXT               | FLOAT              |
| EAN             | TEXT               | VARCHAR(?)         |
| product_code    | TEXT               | VARCHAR(?)         |
| date_added      | TEXT               | DATE               |
| uuid            | TEXT               | UUID               |
| still_available | TEXT               | BOOL               |
| weight_class    | TEXT               | VARCHAR(?)         |
+-----------------+--------------------+--------------------+

*/

SELECT * FROM dim_products;

-- product_price, weight
ALTER TABLE dim_products
ALTER COLUMN product_price TYPE FLOAT USING product_price::double precision,
ALTER COLUMN weight TYPE FLOAT USING weight::double precision;

-- length of EAN
ALTER TABLE dim_products
ALTER COLUMN "EAN" TYPE TEXT
SELECT MAX(LENGTH("EAN")) AS max_length
FROM dim_products;

-- edit VARCHAR accordingly
ALTER TABLE dim_products
ALTER COLUMN "EAN" TYPE VARCHAR(17)


-- length of product_code
ALTER TABLE dim_products
ALTER COLUMN product_code TYPE TEXT
SELECT MAX(LENGTH(product_code)) AS max_length
FROM dim_products;

-- edit VARCHAR accordingly
ALTER TABLE dim_products
ALTER COLUMN product_code TYPE VARCHAR(11);


-- date_added
ALTER TABLE dim_products
ALTER COLUMN date_added TYPE DATE USING date_added::date;

-- UUID
ALTER TABLE dim_products
ALTER COLUMN uuid TYPE UUID USING uuid::uuid;

-- still_available processed below, as code is longer

-- length of weight_class
SELECT MAX(LENGTH(weight_class)) AS max_length
FROM dim_products;

-- edit VARCHAR accordingly
ALTER TABLE dim_products
ALTER COLUMN weight_class TYPE VARCHAR(14);


-- rename 'removed' 
ALTER TABLE dim_products
RENAME removed TO still_available

/*
SELECT still_available, COUNT(*) AS frequency
FROM dim_products
GROUP BY still_available
ORDER BY frequency DESC;
*/

-- create new column, will rename to still_available later on...
ALTER TABLE dim_products
ADD COLUMN is_available BOOLEAN;

-- n.b. contains typo '_avaliable', since this is present in source data:
UPDATE dim_products
SET is_available = (
    CASE
        WHEN still_available = 'Still_avaliable' THEN TRUE
        WHEN still_available = 'Removed' THEN FALSE
    END
);

-- drop original and rename is_available to 'still_available'
ALTER TABLE dim_products DROP COLUMN still_available
ALTER TABLE dim_products 
RENAME is_available TO still_available;


-- Check data types
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_products' 
AND column_name IN ('product_price',
		'weight',
		'EAN',
		'product_code',
		'date_added',
		'uuid',
		'still_available',
		'weight_class'			
)
ORDER BY ordinal_position;




