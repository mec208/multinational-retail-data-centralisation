/*
Sales would like the get an accurate metric for how 
quickly the company is making sales.

Determine 
the average time taken between each sale 
grouped by year

the query should return the following information:

 +------+-------------------------------------------------------+
 | year |                           actual_time_taken           |
 +------+-------------------------------------------------------+
 | 2013 | "hours": 2, "minutes": 17, "seconds": 12, "millise... |
 | 1993 | "hours": 2, "minutes": 15, "seconds": 35, "millise... |
 | 2002 | "hours": 2, "minutes": 13, "seconds": 50, "millise... | 
 | 2022 | "hours": 2, "minutes": 13, "seconds": 6,  "millise... |
 | 2008 | "hours": 2, "minutes": 13, "seconds": 2,  "millise... |
 +------+-------------------------------------------------------+
 
Hint: You will need the SQL command LEAD.
*/


-- join orders and dates, and calculate time gap
SELECT  year,
        combined_datetime,
        LEAD(combined_datetime) OVER (ORDER BY combined_datetime) AS next_combined_datetime,
        LEAD(combined_datetime) OVER (ORDER BY combined_datetime) - combined_datetime AS actual_time_taken
FROM 
    orders_table
JOIN
    dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
ORDER BY   
    combined_datetime ASC


-- use the above as a common table expression, aggregate over year
WITH TimeGaps AS (
    SELECT  dim_date_times.year,
            combined_datetime,
            LEAD(combined_datetime) OVER (ORDER BY combined_datetime) AS next_combined_datetime,
            LEAD(combined_datetime) OVER (ORDER BY combined_datetime) - combined_datetime AS actual_time_taken
    FROM 
        orders_table
    JOIN
        dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
)   

SELECT
    year,
    AVG(actual_time_taken) AS average_time_gap
FROM
    TimeGaps
GROUP BY
    year
ORDER BY
    year;