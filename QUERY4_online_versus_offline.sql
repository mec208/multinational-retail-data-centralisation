/*
The company is looking to increase its online sales.

They want to know how many sales are happening online vs offline.

Calculate how many products were sold and the amount of sales 
made for online and offline purchases.

You should get the following information:

+------------------+-------------------------+----------+
| numbers_of_sales | product_quantity_count  | location |
+------------------+-------------------------+----------+
|            26957 |                  107739 | Web      |
|            93166 |                  374047 | Offline  |
+------------------+-------------------------+----------+
*/



-- orders and store_type
SELECT DISTINCT store_type,
CASE
    WHEN store_type = 'Web Portal' THEN 'Web'
    ELSE 'Offline'
END AS location
FROM dim_store_details
ORDER BY location


-- necessary aggregations from orders table
SELECT  COUNT(*) AS number_of_sales,
        SUM(product_quantity) AS product_quantity_count
FROM 
    orders_table

JOIN 
    dim_products ON orders_table.product_code = dim_products.product_code 


-- use collapsed store_type as CTE, aggregate over the two levels:
WITH sale_location AS (
    SELECT 
        store_code, store_type,
        CASE
            WHEN store_type = 'Web Portal' THEN 'Web'
            ELSE 'Offline'
        END AS location
    FROM dim_store_details
)
SELECT  sale_location.location,
        COUNT(*) AS number_of_sales,
        SUM(product_quantity) AS product_quantity_count
FROM 
    orders_table
JOIN
    sale_location ON orders_table.store_code = sale_location.store_code
GROUP BY
    sale_location.location
ORDER BY
    sale_location.location;