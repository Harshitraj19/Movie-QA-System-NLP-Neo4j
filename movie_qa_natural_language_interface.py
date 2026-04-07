from neo4j import GraphDatabase

# Neo4j connection
driver = GraphDatabase.driver(
    "neo4j://127.0.0.1:7687",
    auth=("neo4j", "12345678")
)

driver.verify_connectivity()
print("✅ Neo4j connected successfully")


def answer_question(question: str):
    q = question.lower().strip().replace("?", "").replace('"', "")

    with driver.session() as session:

        # -----------------------------
        # DIRECTOR
        # -----------------------------
        if "who directed" in q:
            movie = q.replace("who directed", "").strip()

            result = session.run("""
                MATCH (d:Director)-[:DIRECTED]->(m:Movie)
                WHERE toLower(m.title) CONTAINS $movie
                RETURN d.name AS director
                LIMIT 1
            """, movie=movie)

            row = result.single()
            return f"🎬 Director: {row['director']}" if row else "❌ Not found"

        # -----------------------------
        # ACTORS
        # -----------------------------
        if "who acted in" in q:
            movie = q.replace("who acted in", "").strip()

            result = session.run("""
                MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
                WHERE toLower(m.title) CONTAINS $movie
                RETURN a.name AS actor
                LIMIT 5
            """, movie=movie)

            actors = [r["actor"] for r in result]
            return "👥 Actors: " + ", ".join(actors) if actors else "❌ Not found"

        # -----------------------------
        # GENRE
        # -----------------------------
        if "which movies are" in q:
            genre = q.replace("which movies are", "").strip()

            result = session.run("""
                MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre)
                WHERE toLower(g.name) CONTAINS $genre
                RETURN m.title AS movie
                LIMIT 10
            """, genre=genre)

            movies = [r["movie"] for r in result]
            return "🎭 Movies: " + ", ".join(movies) if movies else "❌ Not found"

        # -----------------------------
        # TOP 10 MOVIES
        # -----------------------------
        if "top 10 movies" in q:
            result = session.run("""
                MATCH (m:Movie)
                RETURN m.title AS movie, m.rating AS rating
                ORDER BY rating DESC
                LIMIT 10
            """)

            movies = [f"{r['movie']} ({r['rating']})" for r in result]
            return "⭐ Top 10 Movies:\n" + "\n".join(movies)

        # -----------------------------
        # MOVIES BY YEAR
        # -----------------------------
        if "movies in" in q:
            year = q.replace("movies in", "").strip()

            result = session.run("""
                MATCH (m:Movie)
                WHERE m.release_date STARTS WITH $year
                RETURN m.title AS movie
                LIMIT 10
            """, year=year)

            movies = [r["movie"] for r in result]
            return f"📅 Movies in {year}: " + ", ".join(movies) if movies else "❌ Not found"

        # -----------------------------
        # OVERVIEW
        # -----------------------------
        if "tell me about" in q:
            movie = q.replace("tell me about", "").strip()

            result = session.run("""
                MATCH (m:Movie)
                WHERE toLower(m.title) CONTAINS $movie
                RETURN m.title AS title, m.overview AS overview
                LIMIT 1
            """, movie=movie)

            row = result.single()
            return f"🎬 {row['title']}:\n{row['overview']}" if row else "❌ Movie not found"

        # -----------------------------
        # RATING
        # -----------------------------
        if "rating" in q:
            movie = q.replace("what is", "").replace("rating", "").strip()

            result = session.run("""
                MATCH (m:Movie)
                WHERE toLower(m.title) CONTAINS $movie
                RETURN m.title AS title, m.rating AS rating
                LIMIT 1
            """, movie=movie)

            row = result.single()
            return f"⭐ {row['title']} rating: {row['rating']}" if row else "❌ Movie not found"

        # -----------------------------
        # RELEASE DATE
        # -----------------------------
        if "released" in q:
            movie = q.replace("when was", "").replace("released", "").strip()

            result = session.run("""
                MATCH (m:Movie)
                WHERE toLower(m.title) CONTAINS $movie
                RETURN m.title AS title, m.release_date AS date
                LIMIT 1
            """, movie=movie)

            row = result.single()
            return f"📆 {row['title']} released on {row['date']}" if row else "❌ Movie not found"

        return "❌ Sorry, question type not supported."


print("\n🎬 Movie QA System Ready!")
print("Examples:")
print(" - Who directed Titanic?")
print(" - Who acted in Titanic?")
print(" - Which movies are Action?")
print(" - Show top 10 movies")
print(" - Movies in 2010?")
print(" - Tell me about Titanic")
print(" - What is Titanic rating?")
print(" - When was Titanic released?")
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