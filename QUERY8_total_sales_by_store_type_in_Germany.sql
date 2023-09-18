/*
The sales team is looking to expand their territory in Germany. 
Determine which type of store is generating the most sales in Germany.

The query will return:

+--------------+-------------+--------------+
| total_sales  | store_type  | country_code |
+--------------+-------------+--------------+
|   198373.57  | Outlet      | DE           |
|   247634.20  | Mall Kiosk  | DE           |
|   384625.03  | Super Store | DE           |
|  1109909.59  | Local       | DE           |
+--------------+-------------+--------------+

*/


-- get sales by store_type
-- HAVING to filter after GROUP BY
SELECT
    ROUND(SUM(dim_products.product_price * orders_table.product_quantity)::numeric, 2) AS store_type_sales,
    dim_store_details.store_type,
    dim_store_details.country_code
FROM 
    orders_table
JOIN 
    dim_products ON orders_table.product_code = dim_products.product_code
JOIN
    dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY
    dim_store_details.country_code,
    dim_store_details.store_type
HAVING
    dim_store_details.country_code = 'DE'
ORDER BY    
    store_type_sales ASC;