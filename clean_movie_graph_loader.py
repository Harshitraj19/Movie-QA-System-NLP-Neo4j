import pandas as pd
import ast
from neo4j import GraphDatabase
from tqdm import tqdm

# Load both datasets
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# Merge on movie id
df = movies.merge(credits, left_on="id", right_on="movie_id")

# Neo4j connection
driver = GraphDatabase.driver(
    "neo4j://127.0.0.1:7687",
    auth=("neo4j", "12345678")
)


def extract_names(text):
    try:
        items = ast.literal_eval(text)
        return [item["name"] for item in items]
    except:
        return []


def extract_director(text):
    try:
        crew = ast.literal_eval(text)
        for person in crew:
            if person["job"] == "Director":
                return person["name"]
    except:
        return None


with driver.session() as session:
    # Clear old graph
    session.run("MATCH (n) DETACH DELETE n")

    for _, row in tqdm(df.iterrows(), total=len(df)):
        title = str(row["title_x"]).strip()
        release_date = str(row["release_date"]).strip()
        rating = row["vote_average"]
        overview = str(row["overview"]).strip()

        genres = extract_names(row["genres"])
        actors = extract_names(row["cast"])[:5]
        director = extract_director(row["crew"])

        # Create movie node
        session.run("""
            MERGE (m:Movie {title:$title})
            SET m.release_date=$release_date,
                m.rating=$rating,
                m.overview=$overview
        """, title=title,
           release_date=release_date,
           rating=rating,
           overview=overview)

        # Genre nodes
        for genre in genres:
            session.run("""
                MERGE (g:Genre {name:$genre})
                MERGE (m:Movie {title:$title})
                MERGE (m)-[:BELONGS_TO]->(g)
            """, genre=genre, title=title)

        # Actor nodes
        for actor in actors:
            session.run("""
                MERGE (a:Actor {name:$actor})
                MERGE (m:Movie {title:$title})
                MERGE (a)-[:ACTED_IN]->(m)
            """, actor=actor, title=title)

        # Director node
        if director:
            session.run("""
                MERGE (d:Director {name:$director})
                MERGE (m:Movie {title:$title})
                MERGE (d)-[:DIRECTED]->(m)
            """, director=director, title=title)

print("✅ Full Movie Graph Ready")
driver.close()