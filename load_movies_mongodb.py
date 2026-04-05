import pandas as pd
from pymongo import MongoClient

df = pd.read_csv("tmdb_5000_movies.csv")

client = MongoClient("mongodb://localhost:27017/")
db = client["MoviesDB"]
movies_collection = db["movies"]

movies_collection.drop()
movies_collection.insert_many(df.to_dict("records"))

print(f"✅ {len(df)} movies inserted into MongoDB")