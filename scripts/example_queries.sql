-- Find the top 5 brands by number of products
SELECT Brand_ID, COUNT(*) as product_count
FROM products
GROUP BY Brand_ID
ORDER BY product_count DESC
LIMIT 5;

-- Find products containing Sodium Fluoride (Assuming ID 1)
SELECT p.Product_Name, pi.Fluoride_ppm
FROM products p
JOIN product_ingredients pi ON p.Product_ID = pi.Product_ID
WHERE pi.Ingredient_ID = 1;
