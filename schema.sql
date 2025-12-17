USE movie_pipeline;

-- Movies table
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255),
    release_year INT,
    director VARCHAR(255),
    imdb_id VARCHAR(50),
    box_office BIGINT
);

-- Ratings table
CREATE TABLE IF NOT EXISTS ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    rating FLOAT,
    rating_timestamp BIGINT,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

-- Genres table
CREATE TABLE IF NOT EXISTS genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    genre VARCHAR(100),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

SELECT * FROM movies;

SELECT * FROM ratings;

SELECT * FROM genres;
