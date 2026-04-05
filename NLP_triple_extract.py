import spacy
import pandas as pd
from pymongo import MongoClient
from tqdm import tqdm

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["MoviesDB"]
movies_collection = db["movies"]
triples_collection = db["triples"]

# Read movies from MongoDB
movies = list(movies_collection.find())
movies_df = pd.DataFrame(movies)


def extract_triples(text, movie_id):
    triples = []

    try:
        doc = nlp(text)

        for sent in doc.sents:
            subject = None
            verb = None
            obj = None

            for token in sent:
                if token.dep_ in ["nsubj", "nsubjpass"]:
                    subject = token.text.lower()

                if token.pos_ == "VERB":
                    verb = token.lemma_.lower()

                if token.dep_ in ["dobj", "pobj", "attr"]:
                    obj = token.text.lower()

            if subject and verb and obj:
                triples.append({
                    "movie_id": movie_id,
                    "subject": subject,
                    "predicate": verb,
                    "object": obj
                })

    except:
        pass

    return triples


all_triples = []

for _, row in tqdm(movies_df.iterrows(), total=len(movies_df)):
    overview = row.get("overview", "")
    movie_id = row.get("id")

    if overview and overview != "unknown":
        triples = extract_triples(overview, movie_id)
        all_triples.extend(triples)

# Save triples to MongoDB
triples_collection.drop()

if all_triples:
    triples_collection.insert_many(all_triples)

print(f"✅ Triple extraction complete. Total triples: {len(all_triples)}")