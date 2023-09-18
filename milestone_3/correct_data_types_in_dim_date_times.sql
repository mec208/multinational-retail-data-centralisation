/*
+-----------------+-------------------+--------------------+
| dim_date_times  | current data type | required data type |
+-----------------+-------------------+--------------------+
| month           | TEXT              | VARCHAR(?)         |
| year            | TEXT              | VARCHAR(?)         |
| day             | TEXT              | VARCHAR(?)         |
| time_period     | TEXT              | VARCHAR(?)         |
| date_uuid       | TEXT              | UUID               |
+-----------------+-------------------+--------------------+
*/

SELECT * FROM dim_date_times

-- length of day
SELECT MAX(LENGTH(day)) AS max_length
FROM dim_date_times;

ALTER TABLE dim_date_times
ALTER COLUMN day TYPE VARCHAR(2);


-- length of month
SELECT MAX(LENGTH(month)) AS max_length
FROM dim_date_times;

ALTER TABLE dim_date_times
ALTER COLUMN month TYPE VARCHAR(2);


-- length of year
SELECT MAX(LENGTH(year)) AS max_length
FROM dim_date_times;

ALTER TABLE dim_date_times
ALTER COLUMN year TYPE VARCHAR(4);


-- length of time_period
SELECT MAX(LENGTH(time_period)) AS max_length
FROM dim_date_times;

ALTER TABLE dim_date_times
ALTER COLUMN time_period TYPE VARCHAR(10);


-- date_uuid
ALTER TABLE dim_date_times
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid;


-- check data types
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_date_times' 
AND column_name IN ('day',
		'month',
		'year',
		'time_period',
		'date_uuid'
)
ORDER BY ordinal_position;