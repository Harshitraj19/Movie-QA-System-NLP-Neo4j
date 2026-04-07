from flask import Flask, request, jsonify, render_template
from neo4j import GraphDatabase
import traceback

app = Flask(__name__)

# ── Neo4j connection ──────────────────────────────────────────────────────────
NEO4J_URI  = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "12345678"

driver = None

def get_driver():
    global driver
    if driver is None:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    return driver


# ── Core QA logic (mirrors movie_qa_natural_language_interface.py) ─────────────
def answer_question(question: str) -> str:
    q = question.lower().strip().replace("?", "").replace('"', "")

    try:
        session = get_driver().session()

        # DIRECTOR
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

        # ACTORS
        if "who acted in" in q or "who starred in" in q or "cast of" in q:
            movie = (q.replace("who acted in", "")
                       .replace("who starred in", "")
                       .replace("cast of", "")
                       .strip())
            result = session.run("""
                MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
                WHERE toLower(m.title) CONTAINS $movie
                RETURN a.name AS actor
                LIMIT 5
            """, movie=movie)
            actors = [r["actor"] for r in result]
            return "👥 Actors: " + ", ".join(actors) if actors else "❌ Not found"

        # GENRE FILTER
        if "which movies are" in q or "movies with genre" in q:
            genre = (q.replace("which movies are", "")
                       .replace("movies with genre", "")
                       .strip())
            result = session.run("""
                MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre)
                WHERE toLower(g.name) CONTAINS $genre
                RETURN m.title AS movie
                LIMIT 10
            """, genre=genre)
            movies = [r["movie"] for r in result]
            return "🎭 Movies: " + ", ".join(movies) if movies else "❌ Not found"

        # TOP 10
        if "top 10 movies" in q or "show top 10" in q:
            result = session.run("""
                MATCH (m:Movie)
                RETURN m.title AS movie, m.rating AS rating
                ORDER BY rating DESC
                LIMIT 10
            """)
            movies = [f"{r['movie']} ({r['rating']})" for r in result]
            return "⭐ Top 10 Movies:\n" + "\n".join(movies)

        # MOVIES BY YEAR
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

        # OVERVIEW
        if "tell me about" in q or "overview of" in q or "about" in q and len(q.split()) <= 5:
            movie = (q.replace("tell me about", "")
                       .replace("overview of", "")
                       .replace("about", "")
                       .strip())
            result = session.run("""
                MATCH (m:Movie)
                WHERE toLower(m.title) CONTAINS $movie
                RETURN m.title AS title, m.overview AS overview
                LIMIT 1
            """, movie=movie)
            row = result.single()
            return f"🎬 {row['title']}:\n{row['overview']}" if row else "❌ Movie not found"

        # RATING
        if "rating" in q:
            movie = (q.replace("what is", "")
                       .replace("rating of", "")
                       .replace("rating", "")
                       .strip())
            result = session.run("""
                MATCH (m:Movie)
                WHERE toLower(m.title) CONTAINS $movie
                RETURN m.title AS title, m.rating AS rating
                LIMIT 1
            """, movie=movie)
            row = result.single()
            return f"⭐ {row['title']} rating: {row['rating']}" if row else "❌ Movie not found"

        # RELEASE DATE
        if "released" in q or "release date" in q:
            movie = (q.replace("when was", "")
                       .replace("released", "")
                       .replace("release date of", "")
                       .strip())
            result = session.run("""
                MATCH (m:Movie)
                WHERE toLower(m.title) CONTAINS $movie
                RETURN m.title AS title, m.release_date AS date
                LIMIT 1
            """, movie=movie)
            row = result.single()
            return f"📆 {row['title']} released on {row['date']}" if row else "❌ Movie not found"

        return "❌ Sorry, question type not supported. Try: 'Who directed X?', 'Who acted in X?', 'Tell me about X', 'What is X rating?', 'Movies in 2010', 'Top 10 movies'"

    except Exception as e:
        return f"⚠️ Error querying database: {str(e)}"


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = (data or {}).get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        answer = answer_question(question)
        return jsonify({"question": question, "answer": answer})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    try:
        get_driver().verify_connectivity()
        return jsonify({"status": "ok", "neo4j": "connected"})
    except Exception as e:
        return jsonify({"status": "error", "neo4j": str(e)}), 500


if __name__ == "__main__":
    print("🎬 Starting Movie QA Flask Server...")
    app.run(debug=True, port=5000)