-- Count reviews per bank

SELECT
    b.bank_name,
    COUNT(*) AS total_reviews
FROM reviews r
JOIN banks b
ON r.bank_id = b.bank_id
GROUP BY b.bank_name;


-- Average rating per bank

SELECT
    b.bank_name,
    AVG(r.rating) AS average_rating
FROM reviews r
JOIN banks b
ON r.bank_id = b.bank_id
GROUP BY b.bank_name;


-- Check for nulls

SELECT *
FROM reviews
WHERE
    review_text IS NULL
    OR rating IS NULL
    OR review_date IS NULL;