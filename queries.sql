USE movie_pipeline;

-- 1. Movie with the Highest Average Rating
SELECT
    m.title,
    AVG(r.rating) AS avg_rating,
    COUNT(r.rating) AS rating_count
FROM movies m
JOIN ratings r
    ON m.movie_id = r.movie_id
GROUP BY m.movie_id, m.title
HAVING COUNT(r.rating) >= 50
ORDER BY avg_rating DESC
LIMIT 1;

-- 2. Top 5 Genres by Average Rating
SELECT
    g.genre,
    AVG(r.rating) AS avg_rating,
    COUNT(*) AS rating_count
FROM genres g
JOIN ratings r
    ON g.movie_id = r.movie_id
GROUP BY g.genre
HAVING COUNT(*) >= 100
ORDER BY avg_rating DESC
LIMIT 5;

-- 3. Director with the Most Movies
SELECT
    director,
    COUNT(*) AS movie_count
FROM movies
WHERE director IS NOT NULL
GROUP BY director
ORDER BY movie_count DESC
LIMIT 1;

-- 4. Average Rating by Release Year
SELECT
    m.release_year,
    AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r
    ON m.movie_id = r.movie_id
WHERE m.release_year IS NOT NULL
GROUP BY m.release_year
ORDER BY m.release_year;

-- Data Coverage Check
SELECT COUNT(*) AS total_movies,
       COUNT(director) AS movies_with_director
FROM movies;



