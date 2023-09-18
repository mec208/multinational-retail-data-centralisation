/*
+---------------------+-------------------+------------------------+
| store_details_table | current data type |   required data type   |
+---------------------+-------------------+------------------------+
| longitude           | TEXT              | FLOAT                  |
| locality            | TEXT              | VARCHAR(255)           |
| store_code          | TEXT              | VARCHAR(?)             |
| staff_numbers       | TEXT              | SMALLINT               |
| opening_date        | TEXT              | DATE                   |
| store_type          | TEXT              | VARCHAR(255) NULLABLE  |
| latitude            | TEXT              | FLOAT                  |
| country_code        | TEXT              | VARCHAR(?)             |
| continent           | TEXT              | VARCHAR(255)           |
+---------------------+-------------------+------------------------+

There is a row that represents the business's website 
change the location column values where they're null to N/A.
*/


SELECT * FROM dim_store_details;

-- latitude, longitude
ALTER TABLE dim_store_details
ALTER COLUMN latitude TYPE FLOAT,
ALTER COLUMN longitude TYPE FLOAT;

-- locality, continent
ALTER TABLE dim_store_details
ALTER COLUMN locality TYPE VARCHAR(255),
ALTER COLUMN continent TYPE VARCHAR(255);

-- store code
ALTER TABLE dim_store_details
ALTER COLUMN store_code TYPE TEXT;
SELECT MAX(LENGTH(store_code)) AS max_length
FROM dim_store_details;
-- edit VARCHAR accordingly
ALTER TABLE dim_store_details
ALTER COLUMN store_code TYPE VARCHAR(12);

-- staff_numbers
ALTER TABLE dim_store_details
ALTER COLUMN staff_numbers TYPE SMALLINT;

-- opening date
ALTER TABLE dim_store_details
ALTER COLUMN opening_date TYPE DATE USING opening_date::date;

-- country_code
ALTER TABLE dim_store_details
ALTER COLUMN country_code TYPE TEXT;
SELECT MAX(LENGTH(country_code)) AS max_length
FROM dim_store_details;
-- edit VARCHAR accordingly
ALTER TABLE dim_store_details
ALTER COLUMN country_code TYPE VARCHAR(2);

-- store_type
ALTER TABLE dim_store_details
ALTER COLUMN store_type TYPE VARCHAR(255);



-- change the location column values where they're null to N/A.
UPDATE dim_store_details
SET locality = 'N/A'
WHERE locality IS NULL;


-- check data types:
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_store_details' 
AND column_name IN (
        'longitude',
		'latitude',
		'store_code',
        'staff_numbers',
        'opening_date',
        'store_type',
        'country_code',
		'continent'
)
ORDER BY ordinal_position;

-- check store_type is NULLABLE:
SELECT column_name, is_nullable
FROM information_schema.columns
WHERE table_name = 'dim_store_details' 
AND column_name = 'store_code';

-- if needed, not NOT NULL constraint
--ALTER TABLE dim_store_details
--ALTER COLUMN store_code DROP NOT NULL;
