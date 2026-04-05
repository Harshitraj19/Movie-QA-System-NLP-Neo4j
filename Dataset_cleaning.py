import pandas as pd
import ast
from pymongo import MongoClient


# STEP 1: READ DATASETS
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

print("Movies shape:", movies.shape)
print("Credits shape:", credits.shape)


# STEP 2: MERGE BOTH FILES
df = movies.merge(credits, left_on="id", right_on="movie_id")

print("Merged shape:", df.shape)


# STEP 3: EXTRACT LIST NAMES
def extract_names(text):
    try:
        items = ast.literal_eval(text)
        return [item["name"].lower() for item in items]
    except:
        return []


# STEP 4: EXTRACT DIRECTOR
def extract_director(text):
    try:
        crew = ast.literal_eval(text)
        return [person["name"].lower() for person in crew if person["job"] == "Director"]
    except:
        return []


# STEP 5: CLEAN COLUMNS
df["genres"] = df["genres"].apply(extract_names)
df["production_companies"] = df["production_companies"].apply(extract_names)
df["production_countries"] = df["production_countries"].apply(extract_names)
df["spoken_languages"] = df["spoken_languages"].apply(extract_names)
df["cast"] = df["cast"].apply(extract_names)
df["director"] = df["crew"].apply(extract_director)

df["overview"] = df["overview"].fillna("unknown").str.lower()
df["title"] = df["title_x"].str.lower()


# STEP 6: FINAL REQUIRED DATA
cleaned_data = df[
    [
        "id",
        "title",
        "overview",
        "genres",
        "production_companies",
        "production_countries",
        "spoken_languages",
        "cast",
        "director",
        "budget",
        "revenue",
        "runtime",
        "vote_average",
        "release_date",
        "popularity"
    ]
]


# STEP 7: SAVE TO MONGODB
client = MongoClient("mongodb://localhost:27017/")
db = client["MoviesDB"]
collection = db["movies"]

collection.drop()

records = cleaned_data.to_dict(orient="records")
collection.insert_many(records)

print("✅ Data successfully inserted into MongoDB")