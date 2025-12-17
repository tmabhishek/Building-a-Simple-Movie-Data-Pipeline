🎬 Movie Data Pipeline – ETL Assignment
📌 Overview

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline using the MovieLens dataset and the OMDb API.
The pipeline ingests movie and rating data from CSV files, enriches movie records using an external API, transforms and normalizes the data, and loads it into a MySQL relational database for analytical use.

The objective of this assignment is to demonstrate data engineering fundamentals, including data modeling, external API integration, ETL design, and SQL-based analytics.

📌 Data Sources

MovieLens Dataset (Small Version)
Source: https://grouplens.org/datasets/movielens/latest/

Files used:

movies.csv

ratings.csv

OMDb API (Open Movie Database)
Website: http://www.omdbapi.com/

Used to enrich movie data with additional attributes such as:

Director

IMDb ID

Box Office information

A free OMDb API key was generated for this project.

🏗️ Architecture & Flow
Extract

Read movies.csv and ratings.csv from the MovieLens dataset

Fetch additional movie details using the OMDb API

Transform

Clean movie titles to improve API matching

Extract release year from movie titles

Handle missing or unmatched API responses gracefully

Normalize genres into a separate table (one genre per row)

Load

Load movies, ratings, and genres into MySQL

Ensure idempotent execution using INSERT IGNORE

📂 Project Structure
movie-data-pipeline/
├── etl.py         # Python ETL pipeline
├── schema.sql     # Database schema
├── queries.sql    # Analytical SQL queries
└── README.md      # Project documentation

🛠️ Technologies Used

Python 3.11

Pandas – CSV processing

Requests – OMDb API integration

MySQL 8.0

MySQL Connector for Python

⚙️ Environment Setup
1️⃣ Prerequisites

Python 3.11 or higher

MySQL Server running locally

MySQL Workbench (optional but recommended)

2️⃣ Install Python Dependencies
pip install pandas requests mysql-connector-python

3️⃣ Database Setup

Run the following commands in MySQL:

CREATE DATABASE movie_pipeline;
USE movie_pipeline;


Then execute all statements in schema.sql to create the required tables:

movies

ratings

genres

▶️ How to Run the Project

Place movies.csv and ratings.csv in the same directory as etl.py

Update MySQL credentials inside etl.py if required

Run the ETL pipeline:

python etl.py

Expected Output
Movies CSV shape: (9742, 3)
Ratings CSV shape: (100836, 4)
Enriched movies shape: (200, 7)
MySQL connected successfully!
Movies loaded
Ratings loaded
Genres loaded
ETL completed successfully

🧠 Design Choices & Assumptions
🔹 API Rate Limiting

The OMDb free tier has request limits

Enrichment is limited to a subset of 200 movies

The pipeline is configurable and can be scaled using batching or a paid API tier

🔹 Handling Missing API Data

Movie titles may not match OMDb exactly

API failures or missing data are handled by inserting NULL values

The pipeline continues execution without failure

🔹 Data Modeling

Genres are normalized into a separate table

Ratings reference movies via foreign keys

Auto-increment IDs are used as surrogate primary keys

🔹 Idempotency

INSERT IGNORE ensures the ETL pipeline can be re-run safely without creating duplicate records

📊 Analytical Queries

All required analytical SQL queries are included in queries.sql, such as:

Highest average rated movie

Top 5 genres by average rating

Director with the most movies

Average movie rating by release year

🚧 Challenges & Solutions
Challenge 1: Movie Title Mismatch

Problem: MovieLens titles often include years or formatting differences
Solution: Titles were cleaned before API calls, and unmatched movies were handled safely

Challenge 2: API Rate Limits

Problem: OMDb free tier enforces request limits
Solution: Limited API calls and introduced delays to avoid throttling

Challenge 3: Large Ratings Dataset

Problem: The dataset contains over 100,000 ratings
Solution: Efficient inserts and idempotent loading logic were used

🚀 Future Improvements

Use IMDb IDs (links.csv) for more accurate API matching

Use batch inserts (executemany) for improved performance

Cache API responses to reduce repeated calls

Add structured logging instead of print statements

Containerize the pipeline using Docker