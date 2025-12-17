# 🎬 Building a Simple Movie Data Pipeline
## 📌 1. Overview

This project implements a basic end-to-end ETL pipeline using the MovieLens dataset enriched with additional movie information from the OMDb API.

The pipeline reads movie and rating data from CSV files, enriches a subset of movies using an external API, transforms and cleans the data, and loads it into a MySQL database for running analytical SQL queries.

The main goal of this project is to demonstrate:
  1. ETL fundamentals
  2. API integration
  3. Relational database design
  4. SQL-based analysis

## 📌 2. Data Sources

#### MovieLens Dataset (Small):
  
  1. movies.csv → movieId, title, genres

  2. ratings.csv → userId, movieId, rating, timestamp

#### OMDb API:
Used to fetch:

  1. Director

  2. IMDb ID

  3. Box Office information

A free OMDb API key was generated for this project.

## 📌 3. Environment Setup & Execution

#### Prerequisites

  Python 3.x

#### MySQL (local instance)

  Install Required Libraries
  
  pip install pandas requests mysql-connector-python

#### Database Setup

  CREATE DATABASE movie_pipeline;
  
  USE movie_pipeline;

  Execute all table creation statements from schema.sql.

#### Run the ETL Pipeline

  python etl.py

## 📌 4. ETL Design & Flow

#### Extract

  1. Read movies.csv and ratings.csv using Pandas.

  2. Fetch movie details from OMDb API for a limited number of movies.

#### Transform

  1. Clean movie titles by removing release years for better API matching.

  2. Extract release year from movie titles.

  3. Convert rating timestamps from UNIX format to MySQL DATETIME.

  4. Handle missing API responses by inserting NULL values.

#### Load

  1. Insert movies, ratings, and genres into MySQL.

  2. Use INSERT IGNORE to avoid duplicate records.

  3. Maintain referential integrity using foreign keys.

## 📌 5. Data Model Explanation

  movies: Stores movie details and enriched metadata.

  ratings: Stores user ratings linked to movies.

  genres: Stores movie-genre mappings.

This normalized design makes analytical queries easier and avoids data duplication.

## 📌 6. Analytical Queries

The following SQL queries were implemented:

  1. Movie with the highest average rating

  2. Top 5 genres by average rating

  3. Director with the most movies

  4. Average movie rating by release year

These queries are included in queries.sql.

## 📌 7. Challenges Faced & Solutions

#### API Rate Limits

  OMDb free API has request limits.

  Solution: Limited API calls and added delays between requests.

#### Movie Title Matching Issues

  Movie titles in the dataset did not always match OMDb.

  Solution: Cleaned titles and handled missing data gracefully.

#### Duplicate Data on Re-Runs

  Running the ETL multiple times could insert duplicates.

  Solution: Used INSERT IGNORE for idempotent inserts.

#### Timestamp Format Issues

  Ratings timestamps were in UNIX format.

  Solution: Converted timestamps to MySQL DATETIME in Python.

## 📌 8. Assumptions

  1. Only a subset of movies is enriched due to API limits.

  2. Missing API values are stored as NULL.

  3. Local MySQL database is used for simplicity.
     
## 📌 9. Possible Improvements

  1. Cache API responses to avoid repeated calls.

  2. Use batch inserts for better performance.

  3. Add logging instead of print statements.

  4. Enrich all movies using IMDb IDs for accuracy.
