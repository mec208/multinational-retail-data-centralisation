/*
+----------------+--------------------+--------------------+
| dim_user_table | current data type  | required data type |
+----------------+--------------------+--------------------+
| first_name     | TEXT               | VARCHAR(255)       |
| last_name      | TEXT               | VARCHAR(255)       |
| date_of_birth  | TEXT               | DATE               |
| country_code   | TEXT               | VARCHAR(?)         |
| user_uuid      | TEXT               | UUID               |
| join_date      | TEXT               | DATE               |
+----------------+--------------------+--------------------+
*/


SELECT * FROM dim_users;

-- first_name, last_name
ALTER TABLE dim_users
ALTER COLUMN first_name TYPE VARCHAR(255),
ALTER COLUMN last_name TYPE VARCHAR(255);

-- date_of_birth
ALTER TABLE dim_users
ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::date;

-- country code
ALTER TABLE dim_users
ALTER COLUMN country_code TYPE TEXT
SELECT MAX(LENGTH(country_code)) AS max_length
FROM dim_users;
ALTER TABLE dim_users
ALTER COLUMN country_code TYPE VARCHAR(2);

-- user_uuid
ALTER TABLE dim_users
ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid;

-- join_date
ALTER TABLE dim_users
ALTER COLUMN join_date TYPE DATE USING join_date::date;


-- check data types:
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_users' 
AND column_name IN ('first_name',
		'last_name',
		'date_of_birth',
		'country_code',
		'user_uuid',
		'join_date'
)
ORDER BY ordinal_position;