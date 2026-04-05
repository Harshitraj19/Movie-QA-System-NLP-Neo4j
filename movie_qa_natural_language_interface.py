from neo4j import GraphDatabase
import re

# -----------------------------
# Neo4j Connection
# -----------------------------
driver = GraphDatabase.driver(
    "neo4j://127.0.0.1:7687",
    auth=("neo4j", "12345678")
)

driver.verify_connectivity()
print("✅ Neo4j connected successfully")


def answer_question(question: str):
    q = question.lower().strip()

    with driver.session() as session:

        # -----------------------------
        # RELEASE DATE
        # -----------------------------
        if "release" in q or "released" in q:
            movie_match = re.search(r'\"([^\"]+)\"', question)

            if movie_match:
                movie = movie_match.group(1)

                result = session.run(
                    """
                    MATCH (m:Movie)
                    WHERE toLower(m.title) = toLower($movie)
                    RETURN m.release_date AS date
                    """,
                    movie=movie
                )

                row = result.single()

                if row and row["date"]:
                    return f"🎬 {movie} was released on {row['date']}"

                return f"❌ Could not find release date for {movie}"

            return '⚠️ Put movie name in quotes, example: "Inception"'


        # -----------------------------
        # RATING
        # -----------------------------
        if "rating" in q or "score" in q:
            movie_match = re.search(r'\"([^\"]+)\"', question)

            if movie_match:
                movie = movie_match.group(1)

                result = session.run(
                    """
                    MATCH (m:Movie)
                    WHERE toLower(m.title) = toLower($movie)
                    RETURN m.rating AS rating
                    """,
                    movie=movie
                )

                row = result.single()

                if row:
                    return f"⭐ {movie} rating is {row['rating']}"

                return f"❌ Could not find rating for {movie}"

            return '⚠️ Put movie name in quotes, example: "Avatar"'


        # -----------------------------
        # MOVIE OVERVIEW
        # -----------------------------
        if "tell me about" in q:
            movie = q.replace("tell me about", "").strip()

            result = session.run(
                """
                MATCH (m:Movie)
                WHERE toLower(m.title) CONTAINS $movie
                RETURN m.title AS title, m.overview AS overview
                LIMIT 1
                """,
                movie=movie
            )

            row = result.single()

            if row:
                return f"🎬 {row['title']}:\n{row['overview']}"

            return "❌ Movie not found"


        # -----------------------------
        # DEFAULT
        # -----------------------------
        return "❌ Sorry, I can answer release date, rating, and movie overview questions only."


print("\n🎬 Movie QA System Ready!")
print('Examples:')
print(' - When was "Inception" released?')
print(' - What is "Avatar" rating?')
print(' - Tell me about Titanic')
print()

while True:
    question = input("Ask your movie question: ")

    if question.lower() == "exit":
        break

    answer = answer_question(question)

    print("\n🤖 Answer:")
    print(answer)
    print("-" * 50)

driver.close()