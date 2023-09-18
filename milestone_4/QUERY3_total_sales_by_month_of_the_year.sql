/*

Query the database to find out which months typically 
have the most sales 

your query should return the following information:

+-------------+-------+
| total_sales | month |
+-------------+-------+
|   673295.68 |     8 |
|   668041.45 |     1 |
|   657335.84 |    10 |
|   650321.43 |     5 |
|   645741.70 |     7 |
|   645463.00 |     3 |
+-------------+-------+

*/


-- join orders and products
SELECT  orders_table.*,
        dim_products.product_price,
        (dim_products.product_price * orders_table.product_quantity) AS total_order_price
FROM 
    orders_table
JOIN 
    dim_products ON orders_table.product_code = dim_products.product_code 


-- join orders and dates
SELECT  orders_table.*,
        dim_date_times.month
FROM 
    orders_table
JOIN
    dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid


-- join both products and dates to orders_table
SELECT  orders_table.*,
        dim_products.product_price,
        dim_date_times.month,
        (dim_products.product_price * orders_table.product_quantity) AS total_order_price
FROM 
    orders_table
JOIN 
    dim_products ON orders_table.product_code = dim_products.product_code
JOIN
    dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid    



-- aggregate (sum) total_order_prices by month
SELECT
    dim_date_times.month,
    ROUND(SUM(dim_products.product_price * orders_table.product_quantity)::numeric, 2) AS total_sales
FROM 
    orders_table
JOIN 
    dim_products ON orders_table.product_code = dim_products.product_code
JOIN
    dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
GROUP BY
    dim_date_times.month
ORDER BY
    CAST(dim_date_times.month AS numeric);