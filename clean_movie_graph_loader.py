import pandas as pd
from neo4j import GraphDatabase
from tqdm import tqdm

df = pd.read_csv("tmdb_5000_movies.csv")

driver = GraphDatabase.driver(
    "neo4j://127.0.0.1:7687",
    auth=("neo4j", "12345678")
)

with driver.session() as session:
    for _, row in tqdm(df.iterrows(), total=len(df)):
        title = str(row.get("title", "")).strip()
        release_date = str(row.get("release_date", "")).strip()
        rating = row.get("vote_average", 0)
        overview = str(row.get("overview", "")).strip()

        if not title:
            continue

        session.run(
            """
            MERGE (m:Movie {title:$title})
            SET m.release_date=$release_date,
                m.rating=$rating,
                m.overview=$overview
            """,
            title=title,
            release_date=release_date,
            rating=rating,
            overview=overview
        )

print("✅ Clean Movie Graph Ready")
driver.close()