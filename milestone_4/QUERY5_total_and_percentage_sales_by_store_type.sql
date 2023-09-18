/*
The sales team wants to know which of the different store types 
generates the most revenue

Find out the total and percentage of sales 
coming from each of the different store types.

The query should return:

+-------------+-------------+---------------------+
| store_type  | total_sales | percentage_total(%) |
+-------------+-------------+---------------------+
| Local       |  3440896.52 |               44.87 |
| Web portal  |  1726547.05 |               22.44 |
| Super Store |  1224293.65 |               15.63 |
| Mall Kiosk  |   698791.61 |                8.96 |
| Outlet      |   631804.81 |                8.10 |
+-------------+-------------+---------------------+
*/


-- get sales by store_type
SELECT
    dim_store_details.store_type,
    ROUND(SUM(dim_products.product_price * orders_table.product_quantity)::numeric, 2) AS store_type_sales
FROM 
    orders_table
JOIN 
    dim_products ON orders_table.product_code = dim_products.product_code
JOIN
    dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY
    dim_store_details.store_type


-- get total sales 
SELECT SUM(dim_products.product_price * orders_table.product_quantity) AS total_all_sales        
FROM 
    orders_table
JOIN 
    dim_products ON orders_table.product_code = dim_products.product_code


-- Full Query: 
-- combine store_type sales and total all sales as CTEs
-- calculate the percentages
WITH StoreTypeSales AS (
    SELECT
        dim_store_details.store_type,
        SUM(dim_products.product_price * orders_table.product_quantity) AS store_type_sales
    FROM 
        orders_table
    JOIN 
        dim_products ON orders_table.product_code = dim_products.product_code
    JOIN
        dim_store_details ON orders_table.store_code = dim_store_details.store_code
    GROUP BY
        dim_store_details.store_type
),

TotalAllSales AS (
    SELECT
        SUM(dim_products.product_price * orders_table.product_quantity) AS total_all_sales
    FROM 
        orders_table
    JOIN 
        dim_products ON orders_table.product_code = dim_products.product_code
)

SELECT  StoreTypeSales.store_type,
        ROUND((StoreTypeSales.store_type_sales)::numeric, 2) AS total_sales,
        ROUND(((StoreTypeSales.store_type_sales/TotalAllSales.total_all_sales)*100)::numeric, 2) AS percentage_of_all_sales
FROM 
    StoreTypeSales
CROSS JOIN
    TotalAllSales























-- jank
SELECT
    dim_store_details.store_type,
    SUM(dim_products.product_price * orders_table.product_quantity) AS total_order_price
FROM 
    orders_table
JOIN 
    dim_products ON orders_table.product_code = dim_products.product_code
JOIN
    dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY
    dim_store_details.store_type    