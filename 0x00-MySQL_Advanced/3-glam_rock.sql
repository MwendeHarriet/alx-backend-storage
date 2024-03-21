-- Lists all bands with Glam rock as their main style, ranked by their longevity
-- Calculate lifespan: if split is null replace it with 2022

SELECT
    band_name,
    (IFNULL(split, 2022) - formed) AS lifespan
FROM metal_bands
WHERE
    style LIKE '%Glam rock%'
ORDER BY
    lifespan DESC;
