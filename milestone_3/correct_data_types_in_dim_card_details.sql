/*
+------------------------+-------------------+--------------------+
|    dim_card_details    | current data type | required data type |
+------------------------+-------------------+--------------------+
| card_number            | TEXT              | VARCHAR(?)         |
| expiry_date            | TEXT              | VARCHAR(?)         |
| date_payment_confirmed | TEXT              | DATE               |
+------------------------+-------------------+--------------------+
*/

-- length of card_number
SELECT MAX(LENGTH(card_number)) AS max_length
FROM dim_card_details;

-- edit VARCHAR accordingly
ALTER TABLE dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(19);



-- length of expiry_date
SELECT MAX(LENGTH(expiry_date)) AS max_length
FROM dim_card_details;

-- edit VARCHAR accordingly
ALTER TABLE dim_card_details
ALTER COLUMN expiry_date TYPE VARCHAR(5);


-- date_payment_confirmed
ALTER TABLE dim_card_details
ALTER COLUMN date_payment_confirmed TYPE DATE 
USING date_payment_confirmed::date;


-- check data types:
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_card_details' 
AND column_name IN (
		'card_number',
		'expiry_date',
		'date_payment_confirmed'
)
ORDER BY ordinal_position;
