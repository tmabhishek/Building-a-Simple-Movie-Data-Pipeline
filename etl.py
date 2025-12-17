import pandas as pd
import requests
import time
import mysql.connector
from datetime import datetime   

# -------------------------
# CONFIG
# -------------------------
API_KEY = "2d1c8422"
MAX_API_CALLS = 400

# -------------------------
# EXTRACT: Read CSV files
# -------------------------
movies_df = pd.read_csv("movies.csv")
ratings_df = pd.read_csv("ratings.csv")

print("Movies CSV shape:", movies_df.shape)
print("Ratings CSV shape:", ratings_df.shape)

# -------------------------
# EXTRACT: OMDb API function
# -------------------------
def fetch_movie_details(title):
    clean_title = title.split("(")[0].strip()
    url = "http://www.omdbapi.com/"
    params = {
        "t": clean_title,
        "apikey": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("Response") == "True":
            return {
                "director": data.get("Director"),
                "imdb_id": data.get("imdbID"),
                "box_office": data.get("BoxOffice")
            }
        else:
            return {
                "director": None,
                "imdb_id": None,
                "box_office": None
            }
    except Exception:
        return {
            "director": None,
            "imdb_id": None,
            "box_office": None
        }

# -------------------------
# TRANSFORM: Clean & Enrich
# -------------------------
movies_subset = movies_df.head(MAX_API_CALLS).copy()

# Extract release year
movies_subset["release_year"] = movies_subset["title"].str.extract(r"\((\d{4})\)")

# Fetch OMDb data
omdb_results = []

for title in movies_subset["title"]:
    omdb_results.append(fetch_movie_details(title))
    time.sleep(1)   # prevent API rate limit

omdb_df = pd.DataFrame(omdb_results)

# Combine MovieLens + OMDb
movies_enriched = pd.concat(
    [movies_subset.reset_index(drop=True), omdb_df],
    axis=1
)

print("Enriched movies shape:", movies_enriched.shape)

# -------------------------
# LOAD: MySQL connection
# -------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abhi@4463",
    database="movie_pipeline"
)
cursor = conn.cursor()
print("MySQL connected successfully!")

# -------------------------
# LOAD: Movies table
# -------------------------
movie_insert = """
INSERT IGNORE INTO movies
(movie_id, title, release_year, director, imdb_id, box_office)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for _, row in movies_enriched.iterrows():
    cursor.execute(
        movie_insert,
        (
            row["movieId"],
            row["title"],
            row["release_year"],
            row["director"],
            row["imdb_id"],
            None
        )
    )

conn.commit()
print("Movies loaded")

# -------------------------
# LOAD: Ratings table 
# -------------------------
rating_insert = """
INSERT IGNORE INTO ratings
(user_id, movie_id, rating, rating_timestamp)
VALUES (%s, %s, %s, %s)
"""

for _, row in ratings_df.iterrows():
    rating_datetime = datetime.fromtimestamp(row["timestamp"])  
    cursor.execute(
        rating_insert,
        (
            row["userId"],
            row["movieId"],
            row["rating"],
            rating_datetime
        )
    )

conn.commit()
print("Ratings loaded")

# -------------------------
# LOAD: Genres table
# -------------------------
genre_insert = """
INSERT IGNORE INTO genres (movie_id, genre)
VALUES (%s, %s)
"""

for _, row in movies_df.iterrows():
    if row["genres"] != "(no genres listed)":
        for g in row["genres"].split("|"):
            cursor.execute(genre_insert, (row["movieId"], g))

conn.commit()
print("Genres loaded")

cursor.close()
conn.close()
print("ETL completed successfully")
