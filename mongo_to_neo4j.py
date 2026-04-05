from pymongo import MongoClient
from neo4j import GraphDatabase
from tqdm import tqdm
import re

# -----------------------------
# MongoDB Connection
# -----------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["MoviesDB"]
triples_collection = db["triples"]

triples = list(triples_collection.find())

print(f"✅ Loaded {len(triples)} triples from MongoDB")

# -----------------------------
# Neo4j Connection
# -----------------------------
driver = GraphDatabase.driver(
    "neo4j://127.0.0.1:7687",
    auth=("neo4j", "12345678")
)

driver.verify_connectivity()
print("✅ Neo4j connected successfully")

# -----------------------------
# Insert into Neo4j
# -----------------------------
with driver.session() as session:
    # clear old graph first
    session.run("MATCH (n) DETACH DELETE n")
    print("🗑️ Old graph deleted")

    for triple in tqdm(triples):
        subject = str(triple.get("subject", "")).strip()
        obj = str(triple.get("object", "")).strip()
        predicate = str(triple.get("predicate", "")).strip()

        # Skip empty nodes
        if not subject or not obj:
            continue

        # Clean relationship type
        predicate = re.sub(r'[^A-Za-z0-9_]', '_', predicate.upper())

        # Fallback relationship
        if not predicate or predicate == "_":
            predicate = "RELATED_TO"

        query = f"""
        MERGE (s:Entity {{name: $subject}})
        MERGE (o:Entity {{name: $object}})
        MERGE (s)-[:{predicate}]->(o)
        """

        session.run(query, subject=subject, object=obj)

print("✅ Neo4j graph created successfully!")
driver.close()