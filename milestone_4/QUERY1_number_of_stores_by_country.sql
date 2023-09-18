/*
The Operations team would like to know which countries we currently operate in
and which country now has the most stores. 

Perform a query on the database to get the information, it should return the
following information:
*/

SELECT DISTINCT store_type FROM dim_store_details

SELECT country_code  FROM dim_store_details
WHERE store_type LIKE '%Web%'


-- Including Web Store, Based in GB
SELECT country_code, COUNT(*) FROM dim_store_details
GROUP BY country_code
ORDER BY country_code;

-- Not including Web Store
SELECT country_code, COUNT(*) FROM dim_store_details
WHERE store_type NOT LIKE '%Web%'
GROUP BY country_code
ORDER BY country_code;