# 🎬 CineAI — Movie Q&A System with NLP & Neo4j Graph Database

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-2.x-black?logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Neo4j-Graph%20DB-brightgreen?logo=neo4j&logoColor=white" alt="Neo4j" />
  <img src="https://img.shields.io/badge/MongoDB-NoSQL-green?logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/spaCy-NLP-lightblue?logo=spacy&logoColor=white" alt="spaCy" />
  <img src="https://img.shields.io/badge/Dataset-TMDB%205000-orange" alt="TMDB 5000" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License" />
</p>

<p align="center">
  A full-stack <strong>Natural Language Question Answering system</strong> for movies, powered by a Neo4j graph database, NLP-based triple extraction (spaCy), and a sleek dark-mode web interface built with Flask.
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Project Structure](#-project-structure)
- [Graph Database Schema](#-graph-database-schema)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [Supported Question Types](#-supported-question-types)
- [Pipeline Walkthrough](#-pipeline-walkthrough)
- [API Reference](#-api-reference)
- [Dataset Information](#-dataset-information)
- [Troubleshooting](#-troubleshooting)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**CineAI** is a Movie Question-Answering (QA) system that lets users ask natural language questions about movies and get instant answers — powered by a **Neo4j graph database** storing rich relationships between movies, directors, actors, genres, and more.

The pipeline covers:
1. **Data Ingestion** — Raw TMDB 5000 CSV data is cleaned and stored in MongoDB.
2. **NLP Triple Extraction** — spaCy extracts (subject, predicate, object) triples from movie overviews.
3. **Graph Construction** — Cleaned data and triples are imported into Neo4j as a knowledge graph.
4. **Question Answering** — A Flask web app accepts natural language questions, queries Neo4j with Cypher, and returns human-readable answers.

---

## ✨ Features

- 🔍 **Natural Language Queries** — Ask questions in plain English (e.g., *"Who directed Inception?"*)
- 🕸️ **Graph-Powered Answers** — Uses Neo4j's relationship-based queries for accurate results
- 🧠 **NLP Intent Detection** — Regex-based intent matching + spaCy NER fallback
- 🎬 **Rich Movie Knowledge** — Directors, actors, genres, ratings, release dates, overviews, revenues
- 💬 **Beautiful Chat UI** — Animated dark-mode interface with typing indicators and session statistics
- 🟢 **Health Monitoring** — Live Neo4j connection status indicator
- ⚡ **Fast Cypher Queries** — Efficient graph traversal with LIMIT and indexed lookups
- 📊 **Session Stats** — Tracks questions asked, answered, and average response time

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Web Framework** | Flask (Python) |
| **Graph Database** | Neo4j (Cypher queries) |
| **Document Store** | MongoDB |
| **NLP Library** | spaCy (`en_core_web_sm`) |
| **Data Processing** | Pandas, AST |
| **Frontend** | Vanilla HTML, CSS, JavaScript |
| **Fonts** | Google Fonts — Inter, Space Grotesk |
| **Dataset** | TMDB 5000 Movies & Credits |

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA PIPELINE                           │
│                                                                 │
│  TMDB CSVs  ──►  Dataset_cleaning.py  ──►  MongoDB (MoviesDB)   │
│                         │                                       │
│                         ▼                                       │
│               NLP_triple_extract.py  ──►  MongoDB (triples)     │
│                         │                                       │
│                         ▼                                       │
│              clean_movie_graph_loader.py ──►  Neo4j Graph DB    │
│                   (or Neo4j_import.py)                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       WEB APPLICATION                           │
│                                                                 │
│  Browser ──► Flask (app.py) ──► Neo4j Cypher Queries            │
│    │              │                      │                      │
│    │         index.html              Graph DB                   │
│    │         (CineAI UI)         (Movies, Actors,               │
│    └──────────────────────────   Directors, Genres…)            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Movie-QA-System-with-NLP-and-Graph-Databases-main/
│
├── app.py                        # 🚀 Flask web application (main entry point)
├── Question_parser.py            # 🧠 NLP intent detection & entity extraction (spaCy)
├── Query_generator.py            # ⚙️  Cypher query generator (advanced intents)
├── QA_system.py                  # 🔗 QA orchestration wrapper
│
├── Dataset_cleaning.py           # 🧹 Step 1: Clean TMDB CSVs → store in MongoDB
├── load_movies_mongodb.py        # 📥 Alternate MongoDB data loader
├── NLP_triple_extract.py         # 🔬 Step 2: Extract NLP triples from overviews → MongoDB
├── Export_to_csv.py              # 📤 Step 3a: Export MongoDB data to CSV for Neo4j bulk import
├── Neo4j_import.py               # 📤 Step 3b: Import MongoDB data directly into Neo4j
├── clean_movie_graph_loader.py   # 📤 Step 3c: Direct CSV → Neo4j loader (recommended)
│
├── movie_qa_natural_language_interface.py  # CLI-based QA interface
├── test_neo4j.py                 # 🧪 Neo4j connection test script
│
├── templates/
│   └── index.html                # 🎨 CineAI frontend (dark-mode chat UI)
│
├── tmdb_5000_movies.csv          # 📊 TMDB 5000 movies dataset
├── tmdb_5000_credits.csv         # 📊 TMDB 5000 credits dataset
│
└── README.md                     # 📖 This file
```

---

## 🗂️ Graph Database Schema

The Neo4j knowledge graph is structured as follows:

### Node Labels

| Label | Properties |
|---|---|
| `Movie` | `title`, `release_date`, `rating`, `overview` |
| `Actor` | `name` |
| `Director` | `name` |
| `Genre` | `name` |
| `Entity` | `name` (NLP-extracted concepts) |

### Relationships

| Relationship | From → To | Meaning |
|---|---|---|
| `ACTED_IN` | `Actor → Movie` | Actor appeared in the movie |
| `DIRECTED` | `Director → Movie` | Director directed the movie |
| `BELONGS_TO` | `Movie → Genre` | Movie belongs to a genre |
| `HAS_SUBJECT` | `Movie → Entity` | NLP triple subject link |
| `HAS_OBJECT` | `Movie → Entity` | NLP triple object link |
| `RELATION` | `Entity → Entity` | NLP triple predicate |

> **Note:** The advanced `Neo4j_import.py` pipeline also creates `Language`, `Company`, and `Country` nodes with relationships like `SPOKEN_IN`, `PRODUCTION_COMPANY`, `PRODUCED_IN`, `DIRECTED_BY`, etc.

---

## ✅ Prerequisites

Make sure the following are installed before proceeding:

- **Python 3.9+** — [Download](https://www.python.org/downloads/)
- **Neo4j Desktop (or Neo4j Community Server)** — [Download](https://neo4j.com/download/)
- **MongoDB Community Server** — [Download](https://www.mongodb.com/try/download/community) *(required for the data pipeline only)*
- **pip** (Python package manager)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Movie-QA-System-with-NLP-and-Graph-Databases.git
cd Movie-QA-System-with-NLP-and-Graph-Databases
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install flask neo4j pymongo spacy pandas tqdm
```

### 4. Download the spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### 5. Set Up Neo4j

1. Open **Neo4j Desktop** and create a new project/database.
2. Set the database password (default used in this project: `12345678`).
3. Start the database — it runs on `bolt://127.0.0.1:7687` by default.

> ⚠️ If you use a different password, update `NEO4J_PASS` in `app.py` and `auth` in `clean_movie_graph_loader.py`.

### 6. Configure Credentials

Open `app.py` and verify/update the Neo4j credentials:

```python
NEO4J_URI  = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "12345678"   # ← change this to your Neo4j password
```

---

## 🗃️ Data Pipeline (One-Time Setup)

> **Skip this section** if Neo4j already has the movie graph loaded. Jump straight to [Running the Application](#-running-the-application).

The data pipeline runs in 3 steps. The **quickest path** (no MongoDB needed) is **Step 3 only** using `clean_movie_graph_loader.py`.

---

### ⚡ Quick Path — Direct CSV → Neo4j (Recommended)

This single script reads the two CSV files and loads the full graph into Neo4j:

```bash
python clean_movie_graph_loader.py
```

This creates **Movie**, **Actor**, **Director**, and **Genre** nodes with all relationships. The script takes a few minutes depending on your hardware.

---

### 🔬 Full Pipeline (MongoDB + NLP Triples)

Use this if you want NLP triple extraction and richer relationships.

#### Step 1 — Clean & Load Data into MongoDB

Make sure MongoDB is running, then run:

```bash
python Dataset_cleaning.py
```

This reads `tmdb_5000_movies.csv` + `tmdb_5000_credits.csv`, cleans the data, and inserts it into a local MongoDB collection (`MoviesDB.movies`).

#### Step 2 — Extract NLP Triples

```bash
python NLP_triple_extract.py
```

This uses spaCy to extract `(subject, predicate, object)` triples from each movie's overview and stores them in MongoDB (`MoviesDB.triples`).

#### Step 3 — Import to Neo4j

```bash
python Neo4j_import.py
```

This reads from MongoDB and pushes all movies, entities, and triple relationships into Neo4j.

---

## 🚀 Running the Application

After the graph is loaded in Neo4j and Neo4j is running:

```bash
python app.py
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

You should see the **CineAI** dark-mode chat interface. The status indicator in the top right will show **"Neo4j connected"** in green if the database is reachable.

---

## ❓ Supported Question Types

The system supports the following natural language question patterns:

| Question Pattern | Example | What It Returns |
|---|---|---|
| **Who directed [movie]?** | *Who directed Interstellar?* | Director name |
| **Who acted in [movie]?** | *Who acted in Titanic?* | Top 5 actors |
| **Who starred in [movie]?** | *Who starred in Avatar?* | Top 5 actors |
| **Cast of [movie]** | *Cast of Inception* | Top 5 actors |
| **Tell me about [movie]** | *Tell me about The Dark Knight* | Movie overview |
| **Overview of [movie]** | *Overview of Interstellar* | Movie overview |
| **What is [movie] rating?** | *What is Avatar rating?* | IMDb-style rating |
| **When was [movie] released?** | *When was Jurassic Park released?* | Release date |
| **Release date of [movie]** | *Release date of Inception* | Release date |
| **Movies in [year]** | *Movies in 2012* | Up to 10 movie titles |
| **Which movies are [genre]?** | *Which movies are Action?* | Up to 10 movies |
| **Movies with genre [genre]** | *Movies with genre Drama* | Up to 10 movies |
| **Top 10 movies** | *Show top 10 movies* | Top rated movies with scores |

### Quick Example Chips

The UI also provides one-click example chips for fast exploration:

- 🎥 *Who directed Interstellar?*
- 🎭 *Who acted in Titanic?*
- 📖 *Tell me about Inception*
- ⭐ *What is Avatar rating?*
- 📅 *When was Jurassic Park released?*
- 🏆 *Show top 10 movies*
- 🎬 *Which movies are Action?*
- 🗓 *Movies in 2012*

---

## 🔄 Pipeline Walkthrough

```
User types: "Who directed Inception?"
       │
       ▼
  app.py → answer_question()
       │
       ├── Detects "who directed" pattern
       ├── Extracts movie = "inception"
       │
       ▼
  Cypher Query:
    MATCH (d:Director)-[:DIRECTED]->(m:Movie)
    WHERE toLower(m.title) CONTAINS "inception"
    RETURN d.name AS director LIMIT 1
       │
       ▼
  Neo4j returns: "Christopher Nolan"
       │
       ▼
  Flask returns JSON: { "answer": "🎬 Director: Christopher Nolan" }
       │
       ▼
  CineAI UI renders answer in chat bubble
```

---

## 📡 API Reference

The Flask server exposes three endpoints:

### `GET /`
Serves the CineAI web interface.

---

### `POST /ask`

Submit a natural language movie question.

**Request:**
```json
{
  "question": "Who directed Interstellar?"
}
```

**Response (200 OK):**
```json
{
  "question": "Who directed Interstellar?",
  "answer": "🎬 Director: Christopher Nolan"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "No question provided"
}
```

---

### `GET /health`

Check Neo4j connectivity status.

**Response (200 OK — connected):**
```json
{
  "status": "ok",
  "neo4j": "connected"
}
```

**Response (500 — error):**
```json
{
  "status": "error",
  "neo4j": "ServiceUnavailable: Connection refused"
}
```

---

## 📊 Dataset Information

This project uses the publicly available **TMDB 5000 Movie Dataset** from Kaggle.

| File | Size | Contents |
|---|---|---|
| `tmdb_5000_movies.csv` | ~5.4 MB | Movie metadata: title, genres, budget, revenue, overview, ratings, languages, companies, countries |
| `tmdb_5000_credits.csv` | ~38 MB | Cast and crew data: actors, directors, writers |

- **Total movies:** ~4,800
- **Source:** [Kaggle — TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

> ⚠️ These CSV files are included in the repository. Due to their size (~43 MB total), they may take time to clone. If you fork this project, consider using [Git LFS](https://git-lfs.github.com/) or listing them in `.gitignore` and downloading them separately.

---

## 🔧 Troubleshooting

### ❌ `ServiceUnavailable: Connection refused` (Neo4j)

- Make sure **Neo4j Desktop** is open and your database is **started** (green status).
- Verify the bolt port is `7687` (default).
- Check your password in `app.py` matches your Neo4j database password.

### ❌ `Authentication failure` (Neo4j)

- Update `NEO4J_PASS` in `app.py` to match your database's actual password.

### ❌ `ModuleNotFoundError: No module named 'neo4j'`

```bash
pip install neo4j
```

### ❌ `Can't find model 'en_core_web_sm'`

```bash
python -m spacy download en_core_web_sm
```

### ❌ `ServerSelectionTimeoutError` (MongoDB)

- Make sure MongoDB is running:
  ```bash
  # Windows (run as Administrator):
  net start MongoDB
  
  # macOS/Linux:
  sudo systemctl start mongod
  ```

### ❌ Answer returns `❌ Not found` for a valid movie

- The graph may not be fully loaded. Re-run `clean_movie_graph_loader.py`.
- Check that the movie title matches exactly (the system does partial lowercase matching).
- Verify your Neo4j database has data by running in Neo4j Browser:
  ```cypher
  MATCH (m:Movie) RETURN count(m)
  ```

### ❌ `TemplateNotFound: index.html`

- Make sure the `templates/` folder is in the same directory as `app.py`.
- Do not rename or move the `templates/` folder.

---

## 🚀 Future Improvements

- [ ] **Fuzzy title matching** — Handle typos in movie names
- [ ] **More intents** — Support questions about budgets, revenues, production companies
- [ ] **Transformer-based NLU** — Replace regex with BERT/distilBERT for intent classification
- [ ] **Pagination** — Return more results with pagination support
- [ ] **Movie posters** — Integrate TMDB API for poster images
- [ ] **Voice input** — Web Speech API for voice-based queries
- [ ] **Multi-language support** — Detect and answer in multiple languages
- [ ] **Graph visualization** — Interactive Neo4j graph viewer embedded in the UI
- [ ] **Docker deployment** — Containerize Flask + Neo4j + MongoDB for one-command setup
- [ ] **Export chat history** — Allow users to download conversation transcripts

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/your-feature-name`
3. **Make your changes** and commit: `git commit -m "Add: your feature description"`
4. **Push** to your branch: `git push origin feature/your-feature-name`
5. **Open a Pull Request** on GitHub

Please make sure your code:
- Follows PEP 8 style guidelines
- Doesn't break existing question-answering functionality
- Includes brief comments for non-obvious logic

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

---

## 👤 Author

Built with ❤️ as a Big Data & NLP project demonstrating graph-based question answering over a real-world movie dataset.

---

<p align="center">
  <strong>⭐ If you found this project useful, please give it a star on GitHub! ⭐</strong>
</p>
