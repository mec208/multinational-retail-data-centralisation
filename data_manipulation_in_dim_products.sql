/*
The product_price column has a £ character which you need to remove.

The team that handles the deliveries would like 
a new human-readable column added for the weight 
so they can quickly make decisions on delivery weights.

Add a new column weight_class which will contain human-readable 
values based on the weight range of the product.

+--------------------------+-------------------+
| weight_class VARCHAR(?)  | weight range(kg)  |
+--------------------------+-------------------+
| Light                    | < 2               |
| Mid_Sized                | >= 2 - < 40       |
| Heavy                    | >= 40 - < 140     |
| Truck_Required           | => 140            |
+----------------------------+-----------------+
*/

SELECT weight FROM dim_products;


-- remove LEADING £ from product_price
UPDATE dim_products
SET product_price = TRIM(LEADING '£' FROM product_price);


-- First, add the new weight_class column to dim_products 
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(50);

-- Then, update the weight_class column using CASE statement
UPDATE dim_products
SET weight_class = 
    CASE 
        WHEN weight < 2.00 THEN 'Light'
        WHEN weight >= 2.00 AND weight < 40.0 THEN 'Mid_Sized'
        WHEN weight >= 40.0 AND weight < 140.0 THEN 'Heavy'
        WHEN weight >= 140 THEN 'Truck_Required'
    END;